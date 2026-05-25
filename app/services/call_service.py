import uuid
from services.vapi_service import VapiService
from models import CallRequest, CallResponse

class CallService:
    def __init__(self):
        self.vapi_service = VapiService()
        self.active_calls = {}
    
    async def initiate_outbound_call(self, call_request: CallRequest) -> CallResponse:
        call_id = str(uuid.uuid4())
        
        try:
            result = await self.vapi_service.start_call(
                phone_number=call_request.phone_number,
                customer_name=call_request.customer_name,
                appointment_date=call_request.appointment_date
            )
            
            self.active_calls[call_id] = {
                "status": result.get("status", "initiated"),
                "vapi_call_id": result.get("id"),
                "scenario": call_request.scenario,
                "phone": call_request.phone_number
            }
            
            return CallResponse(
                call_id=call_id,
                status="initiated",
                message=f"Call initiated to {call_request.phone_number}"
            )
        except Exception as e:
            return CallResponse(
                call_id=call_id,
                status="failed",
                message=str(e)
            )