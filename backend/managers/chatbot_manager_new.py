"""Chatbot manager for equipment schedule agent."""

import uuid
import asyncio
from typing import Dict, Optional

class ChatbotManager:
    """Manages the interactive chatbot for user queries."""
    
    def __init__(self, connection_string: str):
        """Initialize the chatbot manager.
        
        Args:
            connection_string (str): The database connection string
        """
        self.connection_string = connection_string
        self.chat_sessions = {}
        self._session_lock = asyncio.Lock()
        
    async def process_message(self, session_id: str, message: str) -> Dict:
        """Process a user message and return the appropriate response.
        
        Args:
            session_id (str): The session ID
            message (str): The user message
            
        Returns:
            Dict: Response containing status and message
        """
        try:
            # For testing: return simple response to verify endpoint works
            return {
                "status": "success",
                "response": f"Backend is working! Received: {message}",
                "conversation_id": str(uuid.uuid4())
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "conversation_id": str(uuid.uuid4())
            }
            
    async def cleanup_all_sessions(self) -> None:
        """Cleanup all sessions."""
        self.chat_sessions = {}