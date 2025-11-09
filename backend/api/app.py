"""FastAPI application for the equipment schedule agent."""

import uuid
import json
import asyncio
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config.settings import get_database_connection_string
from managers.chatbot_manager import ChatbotManager
from managers.scheduler import WorkflowScheduler
from api.endpoints import router

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="TARisk API",
    description="API for Political and Trade Risk Analysis",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Add exception handler for 404 errors
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "status": "error",
            "detail": f"Route {request.url.path} not found",
            "requested_path": request.url.path,
            "method": request.method
        }
    )

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Get connection string
connection_string = get_database_connection_string()

# Initialize managers (singletons for the app lifetime)
chatbot_manager = ChatbotManager(connection_string)
workflow_scheduler = WorkflowScheduler(connection_string)

# Import routers
from api.debug_endpoints import debug_router
from api.test_endpoints import test_router

# Include API routers
app.include_router(router, prefix="/api")
app.include_router(debug_router, prefix="/api")
app.include_router(test_router, prefix="/api")
@app.get("/")
async def root():
    """Root endpoint that returns API information."""
    return {
        "message": "Welcome to TARisk API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    """Startup event handler: start background scheduler."""
    try:
        workflow_scheduler.start()
    except Exception as e:
        print(f"Error starting workflow scheduler: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler: stop scheduler and cleanup chat sessions."""
    try:
        workflow_scheduler.stop()
    except Exception as e:
        print(f"Error stopping workflow scheduler: {e}")

    print("Cleaning up all chat sessions...")
    try:
        # ChatbotManager exposes cleanup_all_sessions()
        await chatbot_manager.cleanup_all_sessions()
    except Exception as e:
        print(f"Error during chat session cleanup: {e}")

    # Add a small delay to allow resources to clean up properly
    await asyncio.sleep(0.5)
    print("Shutdown complete")
    
# WebSocket endpoint for chat
@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for chat."""
    await websocket.accept()

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)

            # Process message
            session_id = message_data.get("session_id", str(uuid.uuid4()))
            message = message_data.get("message", "")

            # Get response from chatbot
            try:
                response = await chatbot_manager.process_message(session_id, message)
            except Exception as e:
                response = {"status": "error", "error": str(e)}

            # Send response back to client
            await websocket.send_text(json.dumps(response))

    except WebSocketDisconnect:
        print(f"WebSocket disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        try:
            await websocket.send_text(json.dumps({
                "status": "error",
                "error": str(e)
            }))
        except:
            pass
