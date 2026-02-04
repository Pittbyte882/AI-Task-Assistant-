import os
import json
from anthropic import Anthropic
from typing import List, Dict
from database import Database
from dotenv import load_dotenv
import asyncio

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class AIAgent:
    def __init__(self):
        self.db = Database()
        self.tools = [
            {
                "name": "create_task",
                "description": "Create a new task in the user's to-do list",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The task title"
                        },
                        "description": {
                            "type": "string",
                            "description": "Optional task description"
                        }
                    },
                    "required": ["title"]
                }
            },
            {
                "name": "get_tasks",
                "description": "Get all tasks from the user's to-do list",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "completed": {
                            "type": "boolean",
                            "description": "Filter by completion status (true/false). If not provided, returns all tasks."
                        }
                    }
                }
            },
            {
                "name": "complete_task",
                "description": "Mark a task as completed",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "The ID of the task to complete"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        ]

    async def process_tool_call(self, tool_name: str, tool_input: Dict, user_id: str):
        """Execute tool calls"""
        if tool_name == "create_task":
            return await self.db.create_task(
                user_id=user_id,
                title=tool_input["title"],
                description=tool_input.get("description")
            )
        
        elif tool_name == "get_tasks":
            completed = tool_input.get("completed")
            return await self.db.get_tasks(user_id=user_id, completed=completed)
        
        elif tool_name == "complete_task":
            return await self.db.update_task(
                task_id=tool_input["task_id"],
                completed=True
            )
        
        return None

    async def chat(self, message: str, user_id: str, conversation_history: List[Dict] = None):
        """Main chat function with tool use"""
        
        # Build messages array
        messages = conversation_history if conversation_history else []
        messages.append({"role": "user", "content": message})

        actions_taken = []
        
        # Initial API call
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            tools=self.tools,
            messages=messages
        )

        # Process tool calls
        while response.stop_reason == "tool_use":
            tool_use_block = next(block for block in response.content if block.type == "tool_use")
            
            tool_name = tool_use_block.name
            tool_input = tool_use_block.input
            
            # Execute the tool
            tool_result = await self.process_tool_call(tool_name, tool_input, user_id)
            actions_taken.append(f"Executed: {tool_name}")
            
            # Continue conversation with tool result
            messages.append({"role": "assistant", "content": response.content})
            messages.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_use_block.id,
                    "content": json.dumps(tool_result)
                }]
            })
            
            # Get next response
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                tools=self.tools,
                messages=messages
            )

        # Extract final text response
        final_response = next(
            (block.text for block in response.content if hasattr(block, "text")),
            "I apologize, but I couldn't generate a response."
        )

        return {
            "response": final_response,
            "actions_taken": actions_taken
        }