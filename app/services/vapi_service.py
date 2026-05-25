import httpx
from config import get_settings

settings = get_settings()

class VapiService:
    def __init__(self):
        self.api_key = settings.VAPI_API_KEY
        self.base_url = "https://api.vapi.ai"
    
    async def start_call(self, phone_number: str, customer_name: str = None, appointment_date: str = None):
        """Initiate an outbound call through Vapi"""
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/call",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "assistantId": settings.VAPI_ASSISTANT_ID,
                    "phoneNumber": phone_number,
                    "customer": {
                        "number": phone_number,
                        "name": customer_name or "Valued Customer"
                    },
                    "variables": {
                        "customer_name": customer_name,
                        "appointment_date": appointment_date
                    }
                },
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()