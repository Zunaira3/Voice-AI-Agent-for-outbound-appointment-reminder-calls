from pydantic import BaseModel, Field, validator
from typing import Optional
from enum import Enum

class CallScenario(str, Enum):
    APPOINTMENT_REMINDER = "appointment_reminder"

class CallRequest(BaseModel):
    phone_number: str = Field(..., description="Phone number with country code")
    scenario: CallScenario = CallScenario.APPOINTMENT_REMINDER
    customer_name: Optional[str] = None
    appointment_date: Optional[str] = None
    
    @validator('phone_number')
    def validate_phone(cls, v):
        import re
        if not re.match(r'^\+?[1-9]\d{1,14}$', v):
            raise ValueError('Invalid phone number format. Use +1234567890')
        return v

class CallResponse(BaseModel):
    call_id: str
    status: str
    message: str