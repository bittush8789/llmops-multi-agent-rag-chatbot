import time
import os
import traceback
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from backend.graph import app_graph
from backend.analytics import log_interaction, get_analytics_summary

app = FastAPI(title="TechNova Solutions Multi-Agent AI Assistant")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str
    agents_used: list[str]

# --- API ROUTES FIRST ---

@app.get("/health")
async def health_check():
    return {"status": "online", "company": "TechNova Solutions"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    start_time = time.time()
    try:
        inputs = {"query": request.message}
        result = app_graph.invoke(inputs)
        
        response_time = time.time() - start_time
        answer = result.get("final_answer", "I encountered an error processing your request.")
        agents_used = result.get("agents_used", [])
        
        dept = "unknown"
        if any("hr" in a for a in agents_used): dept = "HR"
        elif any("it" in a for a in agents_used): dept = "IT"
        elif any("product" in a for a in agents_used): dept = "Product"
        elif any("sales" in a for a in agents_used): dept = "Sales"
        elif any("customer" in a for a in agents_used): dept = "Customer Support"
        
        success = "couldn't find" not in answer.lower()
        log_interaction(request.message, agents_used, response_time, success, dept)
        
        return ChatResponse(answer=answer, agents_used=agents_used)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics")
async def analytics_endpoint():
    return get_analytics_summary()

# --- FRONTEND ROUTES LAST ---

# Define frontend directory
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

print(f"Serving frontend from: {FRONTEND_DIR}")

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, 'index.html'))

# Mount everything else in frontend folder to root /
# This will serve style.css, script.js at /style.css, /script.js
app.mount("/", StaticFiles(directory=FRONTEND_DIR), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
