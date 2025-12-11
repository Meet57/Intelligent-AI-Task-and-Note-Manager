# Agent Interface

A simple agent that can interact with your tasks and notes using natural language.

## How it works

The agent:

1. Takes your message (e.g., "Create a task to buy milk")
2. Decides which tools to use (from `app/utils/chroma_tools.py`)
3. Calls the tools (like `create_task`, `search_notes`, etc.)
4. Returns a response

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Use in Flask

```python
from agents.agent_interface import create_agent, run_agent

# Create agent when Flask starts
create_agent()

# Use in a route
@app.route('/agent', methods=['POST'])
def agent_endpoint():
    user_message = request.json.get('message')
    response = run_agent(user_message)
    return {'response': response}
```

### 3. Example usage

```python
# Create a task
response = run_agent("Create a task called 'Buy groceries' with status pending")

# Search notes
response = run_agent("Find all notes about Python")

# Get insights
response = run_agent("What tasks do I have with pending status?")
```

## Available Functions

- `create_agent(system_prompt)` - Create the agent (call once on startup)
- `run_agent(message)` - Send a message and get a response
- `get_tools()` - List available tool names

## Available Tools

The agent can use these tools from `chroma_tools.py`:

**Task Management:**

- `create_task` - Create a new task
- `update_task` - Update an existing task
- `delete_task` - Delete a task
- `search_tasks` - Search tasks by query
- `get_task_chroma` - Get a specific task

**Note Management:**

- `create_note` - Create a new note
- `update_note` - Update an existing note
- `delete_note` - Delete a note
- `search_notes` - Search notes by query
- `get_note_chroma` - Get a specific note

**Relationships:**

- `add_note_to_task` - Link a note to a task
- `remove_note_from_task` - Unlink a note from a task

**Insights:**

- `rag_context_for_query` - Get relevant context for a query

## Configuration

The agent uses OpenRouter with the free Gemma model by default. Set your OpenRouter API key:

```bash
export OPENROUTER_API_KEY="your-key-here"
```

Or in your `.env` file:

```
OPENROUTER_API_KEY=your-key-here
```
