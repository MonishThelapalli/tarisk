"""Automated workflow manager for schedule analysis."""

import os
import uuid
import asyncio

from semantic_kernel.agents import AgentGroupChat
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole

from config import AI_MODEL_NAME, create_genai_client
from agents.instructions import (
    SCHEDULER_AGENT, SCHEDULER_AGENT_INSTRUCTIONS,
    REPORTING_AGENT, REPORTING_AGENT_INSTRUCTIONS
)
from agents.agent_strategies import (
    AutomatedWorkflowSelectionStrategy, 
    AutomatedWorkflowTerminationStrategy
)
from agents.agent_manager import create_or_reuse_agent
from plugins.schedule_plugin import EquipmentSchedulePlugin
from plugins.risk_plugin import RiskCalculationPlugin
from plugins.logging_plugin import LoggingPlugin  # Updated import

class AutomatedWorkflowManager:
    """Manages the automated workflow for schedule analysis."""
    
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.schedule_plugin = EquipmentSchedulePlugin(connection_string)
        self.risk_plugin = RiskCalculationPlugin()
        self.logging_plugin = LoggingPlugin(connection_string)  # Updated to use consolidated logging
    
    async def run_workflow(self):
        """Runs the automated workflow for schedule analysis."""
        # Clear the console
        os.system('cls' if os.name=='nt' else 'clear')
        
        # Get AI model configuration
        try:
            model_name = AI_MODEL_NAME
            print(f"AI model configured: {model_name}")
        except Exception as e:
            print(f"Error reading AI model configuration: {e}")
            return {
                "status": "error",
                "error": f"Failed to read AI model configuration: {str(e)}",
                "workflow_run_id": str(uuid.uuid4())
            }
        
        # Generate a workflow run ID and session ID
        workflow_run_id = str(uuid.uuid4())
        session_id = str(uuid.uuid4())
        print(f"Workflow run ID: {workflow_run_id}")
        print(f"Session ID: {session_id}")
        
        # Log workflow start
        try:
            self.logging_plugin.log_agent_event(
                agent_name="Orchestrator",
                action="Start Workflow",
                result_summary="Starting equipment schedule analysis workflow",
                conversation_id=workflow_run_id
            )
            print("Logged workflow start event")
        except Exception as e:
            print(f"Error logging workflow start: {e}")

        # Create a Gemini/GenAI client using our settings factory and run the workflow
        try:
            # Use the factory imported at module level to create the client
            client = create_genai_client()
            print("Created Google GenAI client for Gemini model calls")

            # Create or reuse the scheduler and reporting agents (compat wrappers)
            # Pass the configured model name we read above so wrappers use the
            # correct Gemini model (keeps compatibility with older callers).
            scheduler_agent = await create_or_reuse_agent(
                client=client,
                agent_name=SCHEDULER_AGENT,
                model_deployment_name=model_name,
                instructions=SCHEDULER_AGENT_INSTRUCTIONS,
                plugins=[self.schedule_plugin, self.risk_plugin, self.logging_plugin]
            )

            reporting_agent = await create_or_reuse_agent(
                client=client,
                agent_name=REPORTING_AGENT,
                model_deployment_name=model_name,
                instructions=REPORTING_AGENT_INSTRUCTIONS,
                plugins=[self.schedule_plugin, self.logging_plugin]
            )

            # Extract optional IDs
            scheduler_agent_id = getattr(getattr(scheduler_agent, 'definition', None), 'id', None)
            reporting_agent_id = getattr(getattr(reporting_agent, 'definition', None), 'id', None)

            print(f"Scheduler agent ready: {scheduler_agent.name} (ID: {scheduler_agent_id})")
            print(f"Reporting agent ready: {reporting_agent.name} (ID: {reporting_agent_id})")

            # Try to create the agent group chat. If this fails (for example
            # because our compatibility wrappers don't match semantic_kernel's
            # Agent model), fall back to a simple sequential invocation using
            # the wrapper objects' async call() method. This keeps the
            # workflow usable without requiring a full adapter implementation.
            print("Creating agent group chat")
            chat = None
            try:
                chat = AgentGroupChat(
                    agents=[scheduler_agent, reporting_agent],
                    termination_strategy=AutomatedWorkflowTerminationStrategy(),
                    selection_strategy=AutomatedWorkflowSelectionStrategy()
                )
            except Exception as e:
                print(f"AgentGroupChat construction failed, will use sequential fallback: {e}")
                import traceback
                traceback.print_exc()

            # Start the workflow with initial instruction that includes thinking context
            print("Creating initial message")
            initial_message = ChatMessageContent(
                role=AuthorRole.USER,
                content=(
                    f"""USER > Please analyze the equipment schedule data and generate a risk report.

When logging your thinking with log_agent_thinking, use these parameters:
- conversation_id: "{workflow_run_id}"
- session_id: "{session_id}"
- model_deployment_name: "{model_name}"
"""
                )
            )

            # Add the initial message to start the chat
            print("Adding message to chat")
            await chat.add_chat_message(initial_message)

            try:
                print("\nStarting equipment schedule analysis...\n")

                # Invoke the chat and capture responses if AgentGroupChat was
                # created successfully. Otherwise, use a simple sequential
                # fallback: run scheduler_agent.call() then reporting_agent.call().
                final_report = ""
                saved_responses = {}
                if chat is not None:
                    print("Invoking AgentGroupChat")
                    async for response in chat.invoke():
                        if response is None or not getattr(response, 'name', None):
                            print("Received empty response, skipping")
                            continue

                        agent_name = response.name
                        print(f"Response from {agent_name}: {getattr(response, 'content', '')[:100]}...")

                        # Store the latest response from each agent
                        saved_responses[agent_name] = response.content

                        # Specifically track the reporting agent's final response
                        if agent_name == REPORTING_AGENT:
                            final_report = response.content
                else:
                    print("Running sequential fallback: scheduler -> reporting")
                    try:
                        # Use the wrapper's async call() to get scheduler output
                        scheduler_input = initial_message.content
                        scheduler_output = await scheduler_agent.call(scheduler_input)
                        print(f"Scheduler output length: {len(str(scheduler_output))}")

                        # Build reporting input with scheduler output included
                        reporting_input = (
                            f"Please generate a professional risk report based on the following scheduler output:\n\n{scheduler_output}\n\n" 
                            f"Use conversation_id: {workflow_run_id} and session_id: {session_id} as context."
                        )

                        reporting_output = await reporting_agent.call(reporting_input)
                        final_report = reporting_output if reporting_output is not None else ""
                        saved_responses[REPORTING_AGENT] = final_report
                        print("Sequential fallback completed")
                    except Exception as fb_e:
                        print(f"Sequential fallback failed: {fb_e}")
                        import traceback
                        traceback.print_exc()
                        final_report = ""

                # Log workflow completion
                try:
                    self.logging_plugin.log_agent_event(
                        agent_name="Orchestrator",
                        action="Complete Workflow",
                        result_summary="Equipment schedule analysis workflow completed successfully",
                        conversation_id=workflow_run_id
                    )
                except Exception as e:
                    print(f"Error logging workflow completion: {e}")

                print("\nWorkflow completed successfully!\n")
                return {
                    "status": "success",
                    "report": final_report,
                    "workflow_run_id": workflow_run_id
                }

            except Exception as e:
                print(f"Error during workflow execution: {e}")
                import traceback
                traceback.print_exc()

                # Log error
                try:
                    self.logging_plugin.log_agent_event(
                        agent_name="Orchestrator",
                        action="Workflow Error",
                        result_summary=f"Error during workflow execution: {str(e)}",
                        conversation_id=workflow_run_id
                    )
                except Exception as log_error:
                    print(f"Failed to log workflow error: {log_error}")

                return {
                    "status": "error",
                    "error": str(e),
                    "workflow_run_id": workflow_run_id
                }

        except Exception as e:
            print(f"Error setting up workflow: {e}")
            import traceback
            traceback.print_exc()

            # Log error
            try:
                self.logging_plugin.log_agent_event(
                    agent_name="Orchestrator",
                    action="Workflow Setup Error",
                    result_summary=f"Error setting up workflow: {str(e)}",
                    conversation_id=workflow_run_id
                )
            except Exception as log_error:
                print(f"Failed to log setup error: {log_error}")

            return {
                "status": "error",
                "error": f"Failed to set up workflow: {str(e)}",
                "workflow_run_id": workflow_run_id
            }
        finally:
            # Close the client if it exists
            if 'client' in locals():
                try:
                    if hasattr(client, 'close') and callable(client.close):
                        client.close()
                        print("Client closed")
                except Exception:
                    pass