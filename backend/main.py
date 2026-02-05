from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ChatRequest, ChatResponse, Task
from agent import AIAgent
from database import Database
import uuid

app = FastAPI(title="AI Task Assistant API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://ai-task-assistant-1pxf.vercel.app",
        "https://*.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = AIAgent()
db = Database()

@app.get("/")
def read_root():
    return {"message": "AI Task Assistant API is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint"""
    try:
        print(f"Received request: {request}")
        
        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or str(uuid.uuid4())
        print(f"Conversation ID: {conversation_id}")
        
        # Get conversation history
        history = await db.get_conversation_history(conversation_id)
        print(f"History: {history}")
        
        # Format history for Claude
        formatted_history = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in history
        ]
        
        # Get AI response
        print("Calling AI agent...")
        result = await agent.chat(
            message=request.message,
            user_id=request.user_id,
            conversation_history=formatted_history
        )
        print(f"AI Result: {result}")
        
        # Save messages
        await db.save_message(conversation_id, "user", request.message, request.user_id)
        await db.save_message(conversation_id, "assistant", result["response"], request.user_id)
        
        return ChatResponse(
            response=result["response"],
            conversation_id=conversation_id,
            actions_taken=result["actions_taken"]
        )
    
    except Exception as e:
        import traceback
        print("ERROR:", str(e))
        print("TRACEBACK:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks/{user_id}")
async def get_tasks(user_id: str):
    """Get all tasks for a user"""
    try:
        tasks = await db.get_tasks(user_id)
        return {"tasks": tasks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tasks")
async def create_task(task: Task):
    """Create a task manually"""
    try:
        result = await db.create_task(
            user_id=task.user_id,
            title=task.title,
            description=task.description
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)