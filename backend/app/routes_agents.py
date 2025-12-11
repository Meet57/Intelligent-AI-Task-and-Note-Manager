from flask import Blueprint, request, jsonify
import datetime

agents_bp = Blueprint("agents", __name__)

from agents.agent_interface import create_agent, run_agent

# Create agent when Flask starts
create_agent()

# Use in a route
@agents_bp.route('/agent', methods=['POST'])
def agent_endpoint():
    user_message = request.json.get('message')
    messages = run_agent(user_message)
    return jsonify({"messages": messages}), 200