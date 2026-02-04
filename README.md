# AI Task Assistant 🤖

An intelligent task management application powered by Claude AI (Anthropic) that allows users to manage their to-do lists through natural conversation.

![AI Task Assistant Demo](screenshot.png)

## 🌟 Features

- **Conversational AI Interface** - Interact with your tasks using natural language
- **Agentic AI** - Claude AI can take actions like creating, reading, and updating tasks
- **Real-time Task Management** - Create, view, and complete tasks through conversation
- **Persistent Storage** - Tasks and conversations saved in Supabase
- **Beautiful UI** - Modern dark theme with smooth animations

## 🛠️ Tech Stack

### Backend
- **Python 3.11+**
- **FastAPI** - Modern async web framework
- **Anthropic Claude AI** - Sonnet 4 model with tool use
- **Supabase** - PostgreSQL database
- **httpx** - Async HTTP client

### Frontend
- **Next.js 15** - React framework
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Lucide Icons** - Beautiful iconography

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or higher
- Node.js 18+ and npm
- Anthropic API key
- Supabase account

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-task-assistant.git
cd ai-task-assistant
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
```

3. **Install dependencies**
```bash
pip install fastapi uvicorn anthropic python-dotenv httpx pydantic
```

4. **Set up environment variables**

Create `.env` file in root:
```env
ANTHROPIC_API_KEY=your_anthropic_api_key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
```

5. **Create database tables**

Run this SQL in Supabase SQL Editor:
```sql
CREATE TABLE tasks (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  completed BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE messages (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  conversation_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  role TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
```

6. **Run the backend**
```bash
cd backend
python main.py
```

Backend will be running at http://localhost:8000

### Frontend Setup

1. **Navigate to frontend**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Run the development server**
```bash
npm run dev
```

Frontend will be running at http://localhost:3000

## 💬 Usage Examples

Try these commands in the chat:
- "Create a task to buy groceries"
- "Show me my tasks"
- "What tasks do I have?"
- "Mark my grocery task as complete"
- "Create a task to finish the project by Friday"

## 🎯 AI Capabilities

The AI assistant can:
- **Create tasks** from natural language descriptions
- **Retrieve tasks** with filtering (all, completed, incomplete)
- **Update tasks** to mark them complete
- **Understand context** from conversation history
- **Handle multiple requests** in one message

## 📁 Project Structure
```
ai-task-assistant/
├── backend/
│   ├── agent.py         # Claude AI agent with tool use
│   ├── database.py      # Supabase database operations
│   ├── main.py          # FastAPI application
│   └── models.py        # Pydantic models
├── frontend/
│   ├── app/
│   │   ├── page.tsx     # Main chat interface
│   │   └── globals.css  # Global styles
│   └── package.json
├── .env                 # Environment variables (not in repo)
├── .gitignore
└── README.md
```

## 🔧 API Endpoints

### POST /chat
Send a message to the AI assistant
```json
{
  "message": "Create a task to buy milk",
  "user_id": "demo-user",
  "conversation_id": "optional-uuid"
}
```

### GET /tasks/{user_id}
Get all tasks for a user

## 🤖 How It Works

1. User sends message through chat interface
2. Frontend calls FastAPI backend
3. Backend uses Claude AI with tool definitions
4. Claude decides which tools to use (create_task, get_tasks, etc.)
5. Backend executes tools and updates database
6. Claude generates natural language response
7. Response sent back to frontend with actions taken

## 🚀 Deployment

### Backend
- Deploy to Railway, Render, or AWS
- Set environment variables
- Ensure Supabase is accessible

### Frontend
- Deploy to Vercel (recommended)
- Automatic deployments from GitHub
- Configure backend API URL

## 📝 License

MIT License - feel free to use this project for learning or your portfolio!

## 🙏 Acknowledgments

- Built with [Anthropic Claude](https://www.anthropic.com/)
- Database by [Supabase](https://supabase.com/)
- UI inspired by modern chat interfaces

## 📧 Contact

Crystal Pittman - pittbyte82@gmail.com

Portfolio: https://crystal-pittman.vercel.app

---

**Note:** This is a demonstration project showcasing agentic AI capabilities for job applications in AI/ML engineering roles.
```

---

## **Step 2: Create .gitignore**

Create `.gitignore` in root:
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
*.egg
*.egg-info/
dist/
build/

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Next.js
frontend/.next/
frontend/out/
frontend/node_modules/
frontend/.env.local

# Logs
*.log
npm-debug.log*