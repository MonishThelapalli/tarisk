"""Debug endpoints for testing connectivity and chat functionality."""
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from config.settings import get_database_connection_string, create_genai_client
from managers.chatbot_manager import ChatbotManager
from api.endpoints import get_chatbot_manager

debug_router = APIRouter()

@debug_router.get("/debug/test")
async def test_endpoint():
    """Test endpoint that always returns a success message."""
    return {
        "status": "success",
        "message": "Backend is responding correctly",
        "timestamp": "2025-10-28"
    }

class DebugMessage(BaseModel):
    """Model for debug messages."""
    message: str
    session_id: str = None

@debug_router.post("/debug/chat")
async def debug_chat(message: DebugMessage, chatbot: ChatbotManager = Depends(get_chatbot_manager)):
    """Debug endpoint for chat that includes detailed error information."""
    try:
        # Use the local stub session by default to avoid full agent initialization
        session_id = message.session_id or "local-test"

        print(f"Debug: Processing message '{message.message}' for session {session_id}")
        
        # Test GenAI client creation
        try:
            genai_client = create_genai_client()
            print("Debug: Successfully created GenAI client")
        except Exception as client_error:
            print(f"Debug: GenAI client creation error: {client_error}")
            return {
                "status": "error",
                "error": f"GenAI client creation failed: {str(client_error)}",
                "client_debug": str(client_error)
            }
        
        # Try to initialize a session explicitly
        try:
            session = await chatbot.initialize_session(session_id)
            print(f"Debug: Session initialized: {session is not None}")
            
            if 'chat' in session:
                print("Debug: Chat object exists in session")
                print(f"Debug: Chat type: {type(session['chat'])}")
            else:
                print("Debug: No chat object in session")
                
        except Exception as session_error:
            print(f"Debug: Session initialization error: {session_error}")
            return {
                "status": "error",
                "error": f"Session initialization failed: {str(session_error)}",
                "session_debug": str(session_error),
            }
        
        # Process the message
        response = await chatbot.process_message(session_id, message.message)
        print(f"Debug: Got response: {response}")
        
        return {
            "status": "success",
            "debug_info": {
                "session_id": session_id,
                "message": message.message,
                "has_chat": 'chat' in session if session else False,
                "response_type": type(response).__name__,
                "genai_client": "initialized successfully"
            },
            "response": response
        }
        
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print(f"Debug: Error processing message: {e}\n{tb}")
        return {
            "status": "error",
            "error": str(e),
            "traceback": tb,
            "debug_info": {
                "session_id": message.session_id,
                "message": message.message
            }
        }

@debug_router.get("/debug/config")
async def debug_config():
    """Test endpoint that returns current configuration status."""
    try:
        genai_client = create_genai_client()
        return {
            "status": "success",
            "config": {
                "database": get_database_connection_string(),
                "genai_client": "initialized successfully",
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }