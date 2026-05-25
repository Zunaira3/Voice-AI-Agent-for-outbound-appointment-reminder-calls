from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

VAPI_API_KEY = os.getenv("VAPI_API_KEY")
VAPI_ASSISTANT_ID = os.getenv("VAPI_ASSISTANT_ID")

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Voice AI Agent</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
            padding: 20px;
        }
        .card {
            background: white;
            padding: 40px;
            border-radius: 20px;
            max-width: 400px;
            width: 100%;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h1 { margin: 0 0 10px 0; }
        p { color: #666; margin-bottom: 20px; }
        input, button {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            box-sizing: border-box;
        }
        button {
            background: #667eea;
            color: white;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover { background: #5a67d8; }
        button:disabled { opacity: 0.6; cursor: not-allowed; }
        .result {
            margin-top: 20px;
            padding: 10px;
            border-radius: 8px;
            display: none;
            font-size: 14px;
        }
        .success {
            background: #d4edda;
            color: #155724;
            display: block;
        }
        .error {
            background: #f8d7da;
            color: #721c24;
            display: block;
        }
        .note {
            font-size: 12px;
            color: #888;
            margin-top: 15px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>📞 Voice AI Agent</h1>
        <p>Appointment Reminder System</p>
        <form id="callForm">
            <input type="tel" id="phone" placeholder="+1234567890" required>
            <input type="text" id="name" placeholder="Customer Name (optional)">
            <input type="text" id="date" placeholder="Appointment Date (optional)">
            <button type="submit">📞 Make Call</button>
        </form>
        <div id="result" class="result"></div>
        <div class="note">Enter your real phone number with country code (e.g., +1 for US)</div>
    </div>
    <script>
        document.getElementById('callForm').onsubmit = async (e) => {
            e.preventDefault();
            const btn = document.querySelector('button');
            const resultDiv = document.getElementById('result');
            
            btn.disabled = true;
            btn.textContent = 'Calling...';
            resultDiv.className = 'result';
            resultDiv.style.display = 'none';
            
            try {
                const res = await fetch('/call', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    body: 'phone_number=' + encodeURIComponent(document.getElementById('phone').value) +
                          '&customer_name=' + encodeURIComponent(document.getElementById('name').value) +
                          '&appointment_date=' + encodeURIComponent(document.getElementById('date').value)
                });
                const data = await res.json();
                
                if (data.success) {
                    resultDiv.className = 'result success';
                    resultDiv.textContent = '✅ ' + data.message;
                } else {
                    resultDiv.className = 'result error';
                    resultDiv.textContent = '❌ ' + data.error;
                }
                resultDiv.style.display = 'block';
            } catch (err) {
                resultDiv.className = 'result error';
                resultDiv.textContent = '❌ Error: ' + err.message;
                resultDiv.style.display = 'block';
            } finally {
                btn.disabled = false;
                btn.textContent = '📞 Make Call';
            }
        };
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTML_PAGE

@app.post("/call")
async def make_call(phone_number: str = Form(...), customer_name: str = Form(""), appointment_date: str = Form("")):
    """
    Initiate an outbound call using Vapi API
    """
    # Validate phone number
    if not phone_number:
        return {"success": False, "error": "Phone number is required"}
    
    try:
        async with httpx.AsyncClient() as client:
            # Prepare the request payload according to Vapi API spec
            payload = {
                "assistantId": VAPI_ASSISTANT_ID,
                "phoneNumber": {
                    "number": phone_number
                },
                "customer": {
                    "number": phone_number,
                    "name": customer_name or "Valued Customer"
                }
            }
            
            print(f"Calling Vapi API with payload: {payload}")
            
            response = await client.post(
                "https://api.vapi.ai/call",
                headers={
                    "Authorization": f"Bearer {VAPI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=30.0
            )
            
            print(f"Vapi response status: {response.status_code}")
            print(f"Vapi response body: {response.text}")
            
            if response.status_code == 201:
                return {"success": True, "message": f"Call initiated to {phone_number}. Your phone will ring shortly."}
            else:
                return {"success": False, "error": f"Vapi error: {response.text}"}
                
    except httpx.TimeoutException:
        return {"success": False, "error": "Request timed out. Please try again."}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)