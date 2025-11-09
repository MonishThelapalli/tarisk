"""Agent creation and management functions."""

async def create_or_reuse_agent(client, agent_name, model_deployment_name, instructions, plugins=None, connections=None):
    """Compatibility shim for agent creation.

    This project previously used Azure AI Projects and AzureAIAgent. The new
    design routes model inference through Google Gemini (via google.genai).
    To minimize invasive changes, this function returns a lightweight
    compatibility object that exposes the expected attributes used by the
    rest of the code (name, definition, plugins, and a `call` method to
    perform inference).

    Parameters are intentionally kept similar to the original function so
    existing callers require minimal changes.
    """
    # The compatibility 'agent' is a thin wrapper around the Gemini model
    class GeminiAgentWrapper:
        def __init__(self, name, model_name, instructions, plugins=None, connections=None):
            self.name = name
            # A minimal 'definition' object to mimic AzureAIAgent.definition
            self.definition = type("_def", (), {"id": f"local-{name}", "name": name, "model": model_name})()
            # Expose .id for compatibility with code that expects agent.id
            try:
                self.id = self.definition.id
            except Exception:
                # Fallback in case definition doesn't provide id
                self.id = f"local-{name}"
            self.plugins = plugins or []
            self.connections = connections
            self.instructions = instructions

        async def call(self, prompt: str, temperature: float = 0.0, max_tokens: int = 1024):
            """Call the configured Gemini model and return text output.

            Uses the google.genai client created via settings.create_genai_client().
            This implementation calls `client.models.generate_content(model=..., contents=...)`
            which is compatible with the installed `google.genai` package. The
            function extracts the first candidate text if present and returns it.
            """
            from config import settings

            # Create a genai client (factory will raise descriptive errors)
            genai_client = settings.create_genai_client()

            # Use the configured model name (AI_MODEL_NAME)
            model_name = model_deployment_name or settings.AI_MODEL_NAME

            try:
                # Prefer the models.generate_content API (installed google.genai exposes this)
                if hasattr(genai_client, 'models') and hasattr(genai_client.models, 'generate_content'):
                    resp = genai_client.models.generate_content(model=model_name, contents=prompt)

                    # resp is a GenerateContentResponse; attempt robust extraction
                    # Typical shape: resp.candidates[0].content.parts -> list of Part(text=...)
                    try:
                        if hasattr(resp, 'candidates') and resp.candidates:
                            first = resp.candidates[0]
                            if hasattr(first, 'content') and hasattr(first.content, 'parts'):
                                parts = first.content.parts
                                texts = []
                                for p in parts:
                                    # parts may be objects with .text
                                    text = getattr(p, 'text', None)
                                    if text is None:
                                        # maybe dict-like
                                        text = p.get('text') if isinstance(p, dict) else None
                                    if text:
                                        texts.append(text)
                                if texts:
                                    return "\n".join(texts)
                            # fallback: try candidate content string fields
                            if hasattr(first, 'text'):
                                return first.text
                    except Exception:
                        pass

                    # Fallback: dict-like extraction
                    try:
                        d = resp
                        if isinstance(d, dict) and 'candidates' in d:
                            return '\n'.join([c.get('content', '') for c in d.get('candidates', [])])
                    except Exception:
                        pass

                    # As last resort, stringify the response
                    return str(resp)

                # If models.generate_content isn't available, try chats.create then generate the next message
                if hasattr(genai_client, 'chats') and hasattr(genai_client.chats, 'create'):
                    chat = genai_client.chats.create(model=model_name, history=[{'author': 'user', 'content': prompt}])
                    try:
                        # chat may expose messages or a last message
                        if hasattr(chat, 'last_response'):
                            return str(chat.last_response)
                    except Exception:
                        pass
                    return str(chat)

                raise RuntimeError('No supported generation method found on genai client')

            except Exception as e:
                # Surface a helpful message
                raise RuntimeError(f"Gemini model call failed: {e}")

    # Create and return the wrapper. We don't manage persistent remote agent
    # resources here; instead this wrapper will perform model inference at
    # runtime using the genai client.
    wrapper = GeminiAgentWrapper(agent_name, model_deployment_name or None, instructions, plugins=plugins, connections=connections)
    # Now create a semantic-kernel-compatible Agent adapter that wraps the
    # GeminiAgentWrapper so it can be used with AgentGroupChat.
    try:
        # Import semantic kernel agent base classes
        from semantic_kernel.agents.agent import Agent, AgentThread, AgentResponseItem
        from semantic_kernel.contents.chat_message_content import ChatMessageContent
        from semantic_kernel.contents.utils.author_role import AuthorRole
    except Exception:
        # semantic-kernel not available; return the simple wrapper
        return wrapper

    import uuid

    class SimpleAgentThread(AgentThread):
        async def _create(self) -> str:
            self._id = str(uuid.uuid4())
            return self._id

        async def _delete(self) -> None:
            self._id = None

        async def _on_new_message(self, new_message: ChatMessageContent) -> None:
            return None

    class SemanticKernelAgentAdapter(Agent):
        # Pydantic-based Agent subclass. We don't override __init__ so
        # KernelBaseModel handles initialization.

        async def get_response(self, messages=None, *, thread: AgentThread | None = None, **kwargs):
            # Normalize messages to a single prompt string
            prompt = ""
            try:
                if messages is None:
                    prompt = ""
                elif isinstance(messages, list):
                    last = messages[-1] if messages else ""
                    prompt = last.content if hasattr(last, 'content') else str(last)
                elif hasattr(messages, 'content'):
                    prompt = messages.content
                else:
                    prompt = str(messages)
            except Exception:
                prompt = str(messages)

            # Call the underlying wrapper for text
            text = await wrapper.call(prompt)

            # Build ChatMessageContent and AgentResponseItem
            cmc = ChatMessageContent(role=AuthorRole.ASSISTANT, content=text, name=self.name)
            thread_obj = thread if thread is not None else SimpleAgentThread()
            # Ensure thread has an id
            try:
                await thread_obj.create()
            except Exception:
                pass

            return AgentResponseItem(message=cmc, thread=thread_obj)

        def invoke(self, messages=None, *, thread: AgentThread | None = None, on_intermediate_message=None, **kwargs):
            async def gen():
                item = await self.get_response(messages, thread=thread, **kwargs)
                yield item

            return gen()

        def invoke_stream(self, messages=None, *, thread: AgentThread | None = None, on_intermediate_message=None, **kwargs):
            # For simplicity, same as invoke
            return self.invoke(messages=messages, thread=thread, on_intermediate_message=on_intermediate_message, **kwargs)

        # Keep compatibility with older code expecting a `call` method
        async def call(self, prompt: str, temperature: float = 0.0, max_tokens: int = 1024):
            resp = await self.get_response(prompt)
            return resp.content

    # Instantiate the adapter and set compatibility fields
    adapter = SemanticKernelAgentAdapter(name=agent_name, instructions=instructions)
    # Provide a minimal 'definition' object for older code paths
    adapter.definition = type("_def", (), {"id": f"local-{agent_name}", "name": agent_name})()
    # Keep a reference to the wrapper for any direct calls
    adapter._wrapped = wrapper

    return adapter

