"""API endpoints for the equipment schedule agent."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
import uuid
import os

from config.settings import get_database_connection_string, create_genai_client
from managers.chatbot_manager import ChatbotManager
from managers.scheduler import WorkflowScheduler

# Create router
router = APIRouter()

# Initialize managers
def get_chatbot_manager():
    """Gets the chatbot manager."""
    connection_string = get_database_connection_string()
    return ChatbotManager(connection_string)

def get_workflow_scheduler():
    """Gets the workflow scheduler."""
    connection_string = get_database_connection_string()
    return WorkflowScheduler(connection_string)

# API Models
class ChatMessage(BaseModel):
    """Model for chat messages."""
    session_id: Optional[str] = None
    message: str

class WorkflowResponse(BaseModel):
    """Model for workflow responses."""
    status: str
    report: Optional[str] = None
    error: Optional[str] = None
    workflow_run_id: Optional[str] = None

class ChatResponse(BaseModel):
    """Model for chat responses."""
    status: str
    response: Optional[str] = None
    error: Optional[str] = None
    conversation_id: Optional[str] = None

# Endpoint to trigger workflow immediately
@router.post("/workflow/run", response_model=WorkflowResponse)
async def run_workflow(scheduler: WorkflowScheduler = Depends(get_workflow_scheduler)):
    """Triggers the workflow to run immediately."""
    result = scheduler.run_now()
    return result

# Endpoint to get status of most recent workflow
@router.get("/workflow/status")
async def get_workflow_status():
    """Gets the status of the most recent workflow."""
    # Here you would implement logic to get the status from the database
    return {"message": "Not implemented yet"}

# REST endpoint for chat (alternative to WebSocket)
@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(message: ChatMessage, chatbot: ChatbotManager = Depends(get_chatbot_manager)):
    """REST endpoint for chat."""
    # Lightweight live-model fallback when no session_id supplied
    if not message.session_id:
        session_id = str(uuid.uuid4())
        try:
            client = create_genai_client()
            model = os.getenv('AI_MODEL_NAME') or 'gemini-2.5-pro'
            if hasattr(client, 'models') and hasattr(client.models, 'generate_content'):
                resp = client.models.generate_content(model=model, contents=message.message)
                out = None
                try:
                    if hasattr(resp, 'candidates') and resp.candidates:
                        first = resp.candidates[0]
                        if hasattr(first, 'content') and hasattr(first.content, 'parts'):
                            parts = first.content.parts
                            texts = [getattr(p, 'text', None) or (p.get('text') if isinstance(p, dict) else None) for p in parts]
                            texts = [t for t in texts if t]
                            if texts:
                                out = '\n'.join(texts)
                        elif hasattr(first, 'text'):
                            out = first.text
                except Exception:
                    pass

                if out is None:
                    try:
                        if isinstance(resp, dict) and 'candidates' in resp:
                            out = '\n'.join([c.get('content', '') for c in resp.get('candidates', [])])
                    except Exception:
                        out = str(resp)

                return {
                    'status': 'success',
                    'response': out or str(resp),
                    'error': None,
                    'conversation_id': session_id,
                    'session_id': session_id
                }
            else:
                return {
                    'status': 'error',
                    'response': None,
                    'error': 'GenAI client is not configured for content generation',
                    'conversation_id': None,
                    'session_id': None
                }
        except Exception as e:
            return {
                'status': 'error',
                'response': None,
                'error': f'Failed to call GenAI client: {e}',
                'conversation_id': None,
                'session_id': None
            }

    # If a session_id was supplied, run the full chatbot manager flow
    session_id = message.session_id
    try:
        response = await chatbot.process_message(session_id, message.message)
        if isinstance(response, dict):
            response.setdefault('session_id', session_id)
        return response
    except Exception as e:
        # Fallback to a single-model generation if the agent flow fails
        try:
            client = create_genai_client()
            model = os.getenv('AI_MODEL_NAME') or 'gemini-2.5-pro'
            if hasattr(client, 'models') and hasattr(client.models, 'generate_content'):
                resp = client.models.generate_content(model=model, contents=message.message)
                out = None
                try:
                    if hasattr(resp, 'candidates') and resp.candidates:
                        first = resp.candidates[0]
                        if hasattr(first, 'content') and hasattr(first.content, 'parts'):
                            parts = first.content.parts
                            texts = [getattr(p, 'text', None) or (p.get('text') if isinstance(p, dict) else None) for p in parts]
                            texts = [t for t in texts if t]
                            if texts:
                                out = '\n'.join(texts)
                        elif hasattr(first, 'text'):
                            out = first.text
                except Exception:
                    pass

                if out is None:
                    try:
                        if isinstance(resp, dict) and 'candidates' in resp:
                            out = '\n'.join([c.get('content', '') for c in resp.get('candidates', [])])
                    except Exception:
                        out = str(resp)

                return {
                    'status': 'success',
                    'response': out or str(resp),
                    'error': None,
                    'conversation_id': session_id,
                    'session_id': session_id
                }
            else:
                return {
                    'status': 'error',
                    'response': None,
                    'error': f'Agent flow failed and GenAI client is unavailable: {e}',
                    'conversation_id': None,
                    'session_id': None
                }
        except Exception as e2:
            return {
                'status': 'error',
                'response': None,
                'error': f'Agent flow failed and fallback generation also failed: {e2}',
                'conversation_id': None,
                'session_id': None
            }

# Endpoint to get risk summary
@router.get("/risks/summary")
async def get_risk_summary():
    """Gets a summary of current schedule risks."""
    connection_string = get_database_connection_string()
    from plugins.schedule_plugin import EquipmentSchedulePlugin
    schedule_plugin = EquipmentSchedulePlugin(connection_string)
    
    result = schedule_plugin.get_risk_summary()
    return result

# Endpoint to get schedule comparison data
@router.get("/schedule/comparison")
async def get_schedule_comparison(equipment_code: str = None, project_code: str = None):
    """Gets schedule comparison data."""
    connection_string = get_database_connection_string()
    from plugins.schedule_plugin import EquipmentSchedulePlugin
    schedule_plugin = EquipmentSchedulePlugin(connection_string)
    
    result = schedule_plugin.get_schedule_comparison_data(
        equipment_code=equipment_code,
        project_code=project_code
    )
    return result


# Simple heatmap endpoint (returns sample data when real data is not available)
@router.get("/heatmap")
async def get_heatmap(conversation_id: Optional[str] = None, session_id: Optional[str] = None):
    """Return heatmap data for a conversation. Currently returns sample data for demo/testing.

    Expected query params: conversation_id, session_id
    """
    # In a full implementation this would look up processed political risk JSON
    # associated with the conversation/session and transform it into the expected
    # heatmap shape. For now return a small sample so the frontend can render.
    sample = [
        {"country": "India", "average_risk": 72, "breakdown": "Govt instability: 40, Protest: 32"},
        {"country": "Pakistan", "average_risk": 65, "breakdown": "Border tensions: 50, Protest: 15"},
        {"country": "Bangladesh", "average_risk": 48, "breakdown": "Economic unrest: 30, Flood risk: 18"},
        {"country": "Nepal", "average_risk": 35, "breakdown": "Political unrest: 20, Infrastructure: 15"},
        {"country": "Sri Lanka", "average_risk": 55, "breakdown": "Economic crisis: 55"}
    ]
    return sample
