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

        token_estimate = len(request.prompt.split()) + len(ai_response.split())

        # FIX: Removed the extra 'database =' which was shadowing the module
        audit_sig = database.log_interaction(
            user_id=request.user_id,
            prompt=request.prompt,
            response=ai_response,
            tokens=token_estimate
        )

        return {
            "status": "logged_and_verified",
            "audit_signature": audit_sig,
            "ai_output": ai_response
        }
    
    except Exception as e:
        # This will now print the actual error to your terminal for debugging
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    # Using 8085 as discussed to avoid Windows port conflicts
    uvicorn.run(app, host="0.0.0.0", port=8085)