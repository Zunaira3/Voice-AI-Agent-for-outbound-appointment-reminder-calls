# Voice-AI-Agent-for-outbound-appointment-reminder-calls
Voice AI Agent - Outbound Appointment Reminder System using FastAPI + Vapi.ai  A production-ready voice AI agent that makes automated outbound calls to confirm or reschedule appointments. Features web UI, FastAPI backend, and Vapi.ai integration for STT/LLM/TTS.


### System Architecture
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Web UI │────▶│ FastAPI │────▶│ Vapi.ai │────▶│ Twilio │
│ (Browser) │ │ Backend │ │ (Voice AI) │ │ (Telephony) │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
│ │
▼ ▼
┌─────────────┐ ┌─────────────┐
│ Call State │ │ Assistant │
│ Storage │ │ Config │
└─────────────┘ └─────────────┘


### Data Flow

1. **User initiates call** via web interface by entering phone number
2. **FastAPI receives request** and validates input
3. **Vapi.ai creates call** using configured assistant
4. **Twilio initiates outbound call** to the provided number
5. **Real-time conversation** flows through Vapi.ai (STT → LLM → TTS)

## Design Decisions

### Why Vapi.ai?
- All-in-one solution for STT, LLM, and TTS
- Built-in telephony integration
- Sub-600ms response times
- Production-ready infrastructure

### Why FastAPI?
- Async support for handling multiple concurrent calls
- Type safety with Pydantic models
- Automatic OpenAPI documentation at `/docs`

### Scenario: Appointment Reminder
The agent (Sarah) confirms appointments or reschedules:
1. Greets and states purpose
2. Confirms appointment date/time
3. Handles rescheduling if needed
4. Closes with polite goodbye

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- Vapi.ai account (free credits included)
- Twilio account with phone number (for outbound calls)

### Installation

```bash
# Clone repository
git clone [https://github.com/YOUR_USERNAME/voice-ai-agent.git]
cd voice-ai-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn httpx python-dotenv
pip install requirements.txt

Environment Configuration
Create .env file:

env
VAPI_API_KEY=your_vapi_private_key
VAPI_ASSISTANT_ID=your_assistant_id

Running the Application
python app/main.py
Open http://localhost:8000 in your browser.

Making a Test Call
Enter a phone number with country code (e.g., +1234567890)

Enter customer name (optional)

Click "Make Call"

Your phone will ring with the AI assistant speaking

