from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import database

app = FastAPI()

# Initialize DB on startup
database.init_db()

class AIRequest(BaseModel):
    user_id: str
    prompt: str

@app.post("/generate")
async def proxy_generate(request: AIRequest):
    # 1. Forward the request to your local Ollama instance
    ollama_url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": request.prompt,
        "stream": False
    }

    try:
        response = requests.post(ollama_url, json=payload)
        response.raise_for_status()
        ai_data = response.json()
        ai_response = ai_data.get("response", "")

        # 2. Extract metadata (In a real app, you'd calculate actual token usage.)
        token_estimate = len(request.prompt.split()) + len(ai_response.split())

        # 3. Create the Imuttable Audit Log
        audit_sig = database = database.log_interaction(
            user_id=request.user_id,
            prompt=request.prompt,
            response=ai_response,
            tokens=token_estimate
        )

        # 4. Return the AI response along with the Audit Signature for transparency
        return {
            "status": "logged_and_verified",
            "audit_signature": audit_sig,
            "ai_output": ai_response
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)