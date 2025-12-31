# Flask CRUD Project with AI Agent

A full-stack task and notes management application with an integrated AI agent powered by LangGraph. The application combines a Flask REST API backend with ChromaDB vector storage and a modern Next.js frontend, featuring natural language interaction through an AI assistant.

## 🎯 Project Overview

This project is an intelligent task and note management system that allows users to:
- Create, read, update, and delete tasks and notes
- Link tasks and notes together to create relationships
- Search using semantic similarity (find by meaning, not just keywords)
- Interact with the system using natural language through an AI agent
- Perform complex operations via conversational chat

## 🏗️ Architecture

### Backend (Flask)
- **Framework**: Flask with Flask-RESTx for API documentation
- **Database**: ChromaDB (vector database with persistent storage)
- **AI Agent**: LangGraph + LangChain with OpenAI/Groq integration
- **API Design**: RESTful API with CORS enabled

### Frontend (Next.js)
- **Framework**: Next.js 16 (App Router) with React 19
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4
- **UI Components**: Custom components with modals and forms
- **Chat Interface**: Markdown rendering with react-markdown

## 🚀 Technologies Used

### Backend Stack

#### Core Framework
- **Flask**: Web framework for Python
- **Flask-CORS**: Cross-Origin Resource Sharing support
- **Flask-RESTx**: REST API framework with automatic Swagger documentation

#### Database & Storage
- **ChromaDB**: Vector database for semantic search and storage
  - Persistent storage in `chroma_persist/` directory
  - Supports semantic similarity search
  - Stores tasks and notes as embedded vectors
  - Enables RAG (Retrieval-Augmented Generation) capabilities

#### AI & Agent System
- **LangGraph**: Framework for building stateful, multi-actor applications
- **LangChain**: Tools and utilities for LLM applications
  - `langchain-core`: Core abstractions
  - `langchain-openai`: OpenAI integration
- **AI Suite (aisuite)**: Unified interface for multiple AI providers
- **OpenAI**: GPT models for AI responses
- **Anthropic**: Claude models support
- **Mistral AI**: Alternative LLM provider
- **Groq**: Fast LLM inference (used in current implementation)

#### Additional Libraries
- **Python-dotenv**: Environment variable management
- **Requests**: HTTP library for external API calls
- **Pandas & NumPy**: Data manipulation utilities

### Frontend Stack

#### Core Framework
- **Next.js 16**: React framework with App Router
- **React 19**: UI library with latest features
- **TypeScript**: Type-safe JavaScript

#### Styling & UI
- **Tailwind CSS 4**: Utility-first CSS framework
- **PostCSS**: CSS processing

#### Additional Features
- **React Markdown**: Markdown rendering for chat messages
- **Remark GFM**: GitHub Flavored Markdown support
- **localStorage**: Client-side chat history persistence

## 📁 Project Structure

```
flask_crud_project/
├── backend/
│   ├── app.py                      # Flask application entry point
│   ├── requirements.txt            # Python dependencies
│   ├── app/
│   │   ├── __init__.py            # Flask app factory
│   │   ├── api.py                 # Health check endpoints
│   │   ├── routes_tasks.py        # Task CRUD endpoints
│   │   ├── routes_notes.py        # Note CRUD endpoints
│   │   ├── routes_agents.py       # AI agent endpoints
│   │   ├── db/
│   │   │   └── chroma_manager.py  # ChromaDB operations manager
│   │   └── utils/
│   │       ├── chroma_tools.py    # Agent-callable tools
│   │       └── seed.py            # Database seeding
│   ├── agents/
│   │   ├── agent_interface.py     # LangGraph agent implementation
│   │   └── README.md              # Agent documentation
│   └── chroma_persist/            # ChromaDB persistent storage
│
└── frontend/
    ├── app/
    │   ├── page.tsx               # Main application page
    │   ├── layout.tsx             # Root layout
    │   └── globals.css            # Global styles
    ├── components/
    │   ├── AgentChat.tsx          # AI chat interface
    │   ├── TaskForm.tsx           # Task creation/edit form
    │   ├── TaskTable.tsx          # Task list display
    │   ├── NoteForm.tsx           # Note creation/edit form
    │   ├── NoteTable.tsx          # Note list display
    │   ├── TasksModal.tsx         # Task details modal
    │   ├── NotesModal.tsx         # Note details modal
    │   └── Navigation.tsx         # Navigation tabs
    ├── utils/
    │   └── api.ts                 # API service layer
    └── types/
        └── index.ts               # TypeScript type definitions
```

## 🔧 How It Works

### Backend Architecture

#### 1. ChromaDB Manager
The `ChromaManager` class serves as the single source of truth for all data operations:
- **Collections**: Maintains two ChromaDB collections (`tasks` and `notes`)
- **Auto-incrementing IDs**: Manages ID generation for tasks and notes
- **CRUD Operations**: Provides create, read, update, delete for both tasks and notes
- **Relationships**: Handles many-to-many relationships between tasks and notes
- **Semantic Search**: Implements vector similarity search for intelligent retrieval

#### 2. REST API Routes
Three main route blueprints:
- **Tasks (`/tasks/`)**: Full CRUD + relationship management
- **Notes (`/notes/`)**: Full CRUD + relationship management
- **Agents (`/agents/agent`)**: AI agent interaction endpoint

#### 3. AI Agent System (LangGraph)
The agent uses a **graph-based workflow**:

```
User Message → LLM → [Decide: Call Tool?]
                          ↓ Yes          ↓ No
                     Execute Tool → Return Result
                          ↓
                     Back to LLM → Final Response
```

**Components**:
- **SimpleAgent Class**: Manages the agent lifecycle
- **StateGraph**: Defines the workflow (LLM → Tools → LLM)
- **Tools**: Functions from `chroma_tools.py` (create_task, search_notes, etc.)
- **LLM Integration**: Uses Groq API with GPT-compatible endpoints

**Available Tools**:
- `create_task`, `update_task`, `delete_task`
- `create_note`, `update_note`, `delete_note`
- `search_tasks`, `search_notes` (semantic search)
- `add_note_to_task`, `remove_note_from_task`
- `rag_context_for_query` (Retrieval-Augmented Generation)

#### 4. Vector Search & RAG
ChromaDB automatically:
- Embeds text content using default embedding models
- Enables semantic search (e.g., "find tasks about shopping" matches "Buy groceries")
- Supports RAG: Agent can retrieve relevant context before answering questions

### Frontend Architecture

#### 1. Single Page Application
- **Tabbed Interface**: Switch between Tasks, Notes, and Agent Chat
- **State Management**: React hooks (useState, useEffect)
- **Real-time Updates**: Automatic refresh after CRUD operations

#### 2. Component Structure
- **Forms**: TaskForm and NoteForm for creating/editing
- **Tables**: Display lists with edit/delete actions
- **Modals**: Show related items (tasks linked to notes, etc.)
- **Chat**: Real-time conversation with AI agent

#### 3. API Service Layer
The `api.ts` module provides:
- **Centralized API calls**: Single source for all backend requests
- **Error handling**: Consistent error management
- **Type safety**: Full TypeScript support

#### 4. Chat Persistence
- Agent chat history stored in browser's `localStorage`
- Persists across page refreshes
- Reset functionality to clear history

## 🎨 Features

### Task Management
- ✅ Create tasks with title, description, status, and deadline
- ✅ Update task details
- ✅ Delete tasks
- ✅ Link notes to tasks
- ✅ Search tasks semantically

### Note Management
- 📝 Create notes with title and content
- 📝 Update note information
- 📝 Delete notes
- 📝 Link tasks to notes
- 📝 Search notes by meaning

### AI Agent Capabilities
- 💬 Natural language interaction
- 💬 Create/update/delete tasks and notes via chat
- 💬 Search and retrieve information
- 💬 Answer questions about your tasks and notes
- 💬 Complex multi-step operations
- 💬 Markdown-formatted responses

### Technical Features
- 🔍 **Semantic Search**: Find items by meaning, not just keywords
- 🔗 **Bidirectional Relationships**: Tasks ↔ Notes linking
- 💾 **Persistent Storage**: ChromaDB with SQLite backend
- 🌐 **CORS Enabled**: Frontend-backend communication
- 📊 **RESTful API**: Clean, standard API design
- 🎯 **Type Safety**: Full TypeScript support in frontend

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**:
```bash
cd backend
```

2. **Create virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
Create a `.env` file in the `backend/` directory:
```env
SECRET_KEY=your_secret_key_here
GROQ_API_KEY=your_groq_api_key_here
# Optional: Add other LLM API keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

5. **Run the Flask server**:
```bash
python app.py
```

The backend will start on `http://127.0.0.1:5000`

### Frontend Setup

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Run the development server**:
```bash
npm run dev
```

The frontend will start on `http://localhost:3000`

### First Run
On first startup, the backend will automatically seed the database with sample data if it's empty.

## 📡 API Endpoints

### Health Check
- `GET /` - API status
- `GET /health` - Health check
- `GET /api/health` - API blueprint health

### Tasks
- `POST /tasks/` - Create task
- `GET /tasks/` - Get all tasks
- `GET /tasks/<id>` - Get task by ID
- `PUT /tasks/<id>` - Update task
- `DELETE /tasks/<id>` - Delete task
- `POST /tasks/<task_id>/notes/<note_id>` - Link note to task
- `DELETE /tasks/<task_id>/notes/<note_id>` - Unlink note from task

### Notes
- `POST /notes/` - Create note
- `GET /notes/` - Get all notes
- `GET /notes/<id>` - Get note by ID
- `PUT /notes/<id>` or `PATCH /notes/<id>` - Update note
- `DELETE /notes/<id>` - Delete note
- `POST /notes/<note_id>/tasks/<task_id>` - Link task to note
- `DELETE /notes/<note_id>/tasks/<task_id>` - Unlink task from note

### Agent
- `POST /agents/agent` - Send message to AI agent
  - Request body: `{"message": "your message"}`
  - Response: `{"messages": [...]}`

## 🤖 Using the AI Agent

### Example Interactions

**Create a task**:
```
User: "Create a task to buy groceries with deadline 2024-01-15"
Agent: Creates the task and confirms
```

**Search for information**:
```
User: "What tasks do I have about shopping?"
Agent: Searches semantically and lists relevant tasks
```

**Complex operations**:
```
User: "Find all pending tasks and create a summary note"
Agent: Searches tasks, analyzes them, creates a note with summary
```

**Update items**:
```
User: "Mark task #3 as completed"
Agent: Updates the task status
```

## 🛠️ Development

### Adding New Tools for the Agent

1. Add function to `backend/app/utils/chroma_tools.py`
2. Include detailed docstring (agent uses this to understand the tool)
3. Agent automatically loads all functions from that module

### Modifying the Frontend

- Components are in `frontend/components/`
- API calls go through `frontend/utils/api.ts`
- Types are defined in `frontend/types/index.ts`
- Styling uses Tailwind CSS classes

### Environment Variables

**Backend** (`.env`):
- `SECRET_KEY`: Flask secret key
- `GROQ_API_KEY`: Groq API key for LLM
- `OPENAI_API_KEY`: (Optional) OpenAI key
- `ANTHROPIC_API_KEY`: (Optional) Anthropic key

## 🔒 Security Notes

- CORS is currently set to allow all origins (`*`) for development
- Update CORS settings for production deployment
- API keys should never be committed to version control
- Use environment variables for sensitive data

## 📝 License

This project is for educational and development purposes.

## 🤝 Contributing

Feel free to fork, modify, and improve this project!

## 📧 Support

For questions or issues, please check the code documentation or create an issue.

---

**Built with ❤️ using Flask, Next.js, ChromaDB, and LangGraph**
