"""Basic test endpoints for debugging."""
from fastapi import APIRouter
from typing import Dict, Any

test_router = APIRouter()

@test_router.get("/test")
async def test_get() -> Dict[str, Any]:
    """Basic GET test endpoint."""
    return {
        "status": "success",
        "message": "GET test endpoint working",
        "path": "/api/test"
    }

@test_router.post("/test")
async def test_post(data: Dict[str, Any]) -> Dict[str, Any]:
    """Basic POST test endpoint."""
    return {
        "status": "success",
        "message": "POST test endpoint working",
        "received_data": data,
        "path": "/api/test"
    }