import sys
import json
import os

from mcp.server.fastmcp import FastMCP
from indexer import load_env
from glean_client import glean_chat

# Load API credentials from env.txt
env_path = os.environ.get("VOLTA_ENV_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "env.txt"))
config = load_env(env_path)

API_TOKEN = config.get("GLEAN_CLIENT_API_TOKEN", "")
INSTANCE = config.get("GLEAN_INSTANCE", "")
act_as_email = config.get("GLEAN_ACT_AS_EMAIL", "")

if not API_TOKEN or not INSTANCE:
    print("ERROR: missing GLEAN_CLIENT_API_TOKEN or GLEAN_INSTANCE in env.txt", file=sys.stderr)
    sys.exit(1)

# Create the MCP server
mcp = FastMCP("volta-coffee-chatbot")

# @mcp.tool() is required — it registers ask_volta so Claude Desktop can see and call it
@mcp.tool()
def ask_volta(question: str) -> str:
    """Ask a question about Volta Coffee Co. internal documentation.
    
    Returns a JSON object with two fields:
    - "answer": the grounded response from Glean
    - "sources": list of source documents used, each with title, url, and doc_id
    
    Always present both the answer AND the sources to the user. 
    Format sources with title, url, and doc_id below answer provided.
    """
    result = glean_chat(API_TOKEN, INSTANCE, question, act_as_email=act_as_email)
    
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    mcp.run(transport="stdio")
