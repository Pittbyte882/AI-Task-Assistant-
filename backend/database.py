import os
import httpx
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

class Database:
    @staticmethod
    async def create_task(user_id: str, title: str, description: str = None):
        """Create a new task"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/tasks",
                json={
                    "user_id": user_id,
                    "title": title,
                    "description": description,
                    "completed": False
                },
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json",
                    "Prefer": "return=representation"
                }
            )
            
            if response.status_code in [200, 201]:
                try:
                    return response.json()
                except:
                    return {"status": "success", "title": title}
            else:
                print(f"Supabase error: {response.status_code} - {response.text}")
                return {"status": "error", "message": response.text}

    @staticmethod
    async def get_tasks(user_id: str, completed: bool = None):
        """Get all tasks for a user"""
        params = {"user_id": f"eq.{user_id}"}
        if completed is not None:
            params["completed"] = f"eq.{completed}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/tasks",
                params=params,
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}"
                }
            )
            return response.json()

    @staticmethod
    async def update_task(task_id: str, completed: bool):
        """Mark task as completed/incomplete"""
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{SUPABASE_URL}/rest/v1/tasks",
                params={"id": f"eq.{task_id}"},
                json={"completed": completed},
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json"
                }
            )
            return response.json()

    @staticmethod
    async def save_message(conversation_id: str, role: str, content: str, user_id: str):
        """Save a chat message"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/messages",
                json={
                    "conversation_id": conversation_id,
                    "role": role,
                    "content": content,
                    "user_id": user_id
                },
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json",
                    "Prefer": "return=representation"
                }
            )
            
            if response.status_code in [200, 201]:
                try:
                    return response.json()
                except:
                    return {"status": "success"}
            else:
                print(f"Supabase error: {response.status_code}")
                return {"status": "error"}

    @staticmethod
    async def get_conversation_history(conversation_id: str, limit: int = 20):
        """Get conversation history"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/messages",
                params={
                    "conversation_id": f"eq.{conversation_id}",
                    "order": "created_at.asc",
                    "limit": limit
                },
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}"
                }
            )
            return response.json()