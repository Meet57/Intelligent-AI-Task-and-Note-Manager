"""Simple agent interface for Flask.

This module provides a simple agent that can:
- Talk to an LLM (using OpenRouter)
- Call tools from chroma_tools.py (like create_task, search_notes, etc.)
- Loop between LLM and tools until the task is done

Usage from Flask:
    from agents.agent_interface import create_agent, run_agent
    
    # On app startup:
    create_agent()
    
    # In a route:
    result = run_agent("Create a task called 'Buy milk'")
"""
import inspect
import os
from typing import Any, Dict, List, Optional, Annotated
from langgraph.graph import StateGraph, END
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import operator
from dotenv import load_dotenv

from app.utils import chroma_tools

# Load environment variables
load_dotenv()

# Simple state: just a list of messages
class AgentState(dict):
    messages: Annotated[List[AnyMessage], operator.add]


# Global agent instance
_agent = None


class SimpleAgent:
    """A simple agent that loops between LLM and tools."""
    
    def __init__(self, system_prompt: str = ""):
        self.system_prompt = system_prompt
        self.tools = self._load_tools()
        
        # Setup LLM (Groq API with tool-calling support)
        self.llm = ChatOpenAI(
            model="openai/gpt-oss-120b",
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1",
            temperature=0.0
        )
        
        # Bind tools to LLM
        from langchain_core.utils.function_calling import convert_to_openai_tool
        tool_schemas = []
        for name, func in self.tools.items():
            tool_schemas.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": func.__doc__ or f"Call the {name} function",
                    "parameters": {
                        "type": "object",
                        "properties": self._get_function_schema(func),
                        "required": []
                    }
                }
            })
        
        self.llm = self.llm.bind(tools=tool_schemas)
        
        # Build the graph
        self.graph = self._build_graph()
    
    def _get_function_schema(self, func) -> dict:
        """Extract parameter schema from function signature."""
        import inspect
        sig = inspect.signature(func)
        properties = {}
        for param_name, param in sig.parameters.items():
            param_type = "string"
            param_description = ""
            
            if param.annotation != inspect.Parameter.empty:
                if param.annotation == int:
                    param_type = "integer"
                elif param.annotation == bool:
                    param_type = "boolean"
                elif param.annotation == str:
                    param_type = "string"
            
            # Add description for common parameters
            if param_name == "query":
                param_description = "A single search query string"
            elif param_name == "top_k":
                param_description = "Number of results to return"
            
            properties[param_name] = {
                "type": param_type,
                "description": param_description
            }
        return properties
    
    def _load_tools(self) -> Dict[str, Any]:
        """Load all functions from chroma_tools as tools."""
        tools = {}
        for name, func in inspect.getmembers(chroma_tools, inspect.isfunction):
            if not name.startswith("_"):
                tools[name] = func
        return tools
    
    def _build_graph(self):
        """Build the StateGraph with LLM and action nodes."""
        graph = StateGraph(AgentState)
        
        # Add nodes
        graph.add_node("llm", self.call_llm)
        graph.add_node("action", self.call_tools)
        
        # Add edges
        graph.add_conditional_edges(
            "llm",
            self.should_continue,
            {True: "action", False: END}
        )
        graph.add_edge("action", "llm")
        
        # Set entry point
        graph.set_entry_point("llm")
        
        return graph.compile()
    
    def call_llm(self, state: AgentState):
        """Call the LLM with current messages."""
        messages = state["messages"]
        
        # Add system prompt if we have one
        if self.system_prompt:
            messages = [SystemMessage(content=self.system_prompt)] + messages
        
        # Call LLM
        response = self.llm.invoke(messages)
        return {"messages": [response]}
    
    def should_continue(self, state: AgentState) -> bool:
        """Check if LLM wants to call a tool."""
        last_message = state["messages"][-1]
        return hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0
    
    def call_tools(self, state: AgentState):
        """Execute the tools requested by LLM."""
        last_message = state["messages"][-1]
        tool_calls = last_message.tool_calls
        
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call.get("args", {})
            
            # Check if tool exists
            if tool_name not in self.tools:
                result = f"Error: Tool '{tool_name}' not found"
            else:
                # Call the tool
                try:
                    result = self.tools[tool_name](**tool_args)
                except Exception as e:
                    result = f"Error calling {tool_name}: {str(e)}"
            
            # Create tool message
            results.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"],
                    name=tool_name
                )
            )
        
        return {"messages": results}
    
    def run(self, user_message: str) -> List[Dict[str, Any]]:
        """Run the agent with a user message and return all messages as JSON array."""
        # Start with user message
        initial_state = {"messages": [HumanMessage(content=user_message)]}
        
        # Run the graph
        final_state = self.graph.invoke(initial_state)
        
        # Convert all messages to JSON-serializable format
        messages_json = []
        for msg in final_state["messages"]:
            if isinstance(msg, HumanMessage):
                messages_json.append({
                    "type": "human",
                    "content": msg.content
                })
            elif isinstance(msg, AIMessage):
                messages_json.append({
                    "type": "ai",
                    "content": msg.content,
                    "tool_calls": getattr(msg, "tool_calls", [])
                })
            elif isinstance(msg, ToolMessage):
                messages_json.append({
                    "type": "tool",
                    "name": msg.name,
                    "content": msg.content
                })
            elif isinstance(msg, SystemMessage):
                messages_json.append({
                    "type": "system",
                    "content": msg.content
                })
        
        return messages_json

def create_agent(system_prompt: str = "You are a helpful assistant that can manage tasks and notes. Use the available tools to help users."):
    """Create the agent. Call this once when Flask starts."""
    global _agent
    _agent = SimpleAgent(system_prompt=system_prompt)
    return _agent


def run_agent(message: str) -> List[Dict[str, Any]]:
    """Run the agent with a message. Returns all messages as JSON array."""
    if _agent is None:
        raise RuntimeError("Agent not created. Call create_agent() first.")
    return _agent.run(message)


def get_tools() -> List[str]:
    """Get list of available tool names."""
    if _agent is None:
        raise RuntimeError("Agent not created. Call create_agent() first.")
    return list(_agent.tools.keys())
