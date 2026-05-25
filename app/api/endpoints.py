from fastapi import APIRouter, HTTPException
from models import CallRequest, CallResponse
from services.call_service import CallService

router = APIRouter()
call_service = CallService()

@router.post("/api/call/initiate", response_model=CallResponse)
async def initiate_call(call_request: CallRequest):
    """Initiate an outbound voice call"""
    return await call_service.initiate_outbound_call(call_request)

@router.get("/api/call/status/{call_id}")
async def get_call_status(call_id: str):
    """Get status of a call"""
    status = call_service.active_calls.get(call_id, {"status": "not_found"})
    return status

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Voice AI Agent"}