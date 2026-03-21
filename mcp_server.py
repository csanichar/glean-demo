import sys
import json
import os

from mcp.server.fastmcp import FastMCP
from indexer import load_env
from glean_client import rag_query

# Load API credentials from env.txt
env_path = os.environ.get("VOLTA_ENV_PATH", "env.txt")
config = load_env(env_path)

API_TOKEN = config.get("GLEAN_SEARCH_API_TOKEN", "")
INSTANCE = config.get("GLEAN_INSTANCE", "")

if not API_TOKEN or not INSTANCE:
    print("ERROR: missing GLEAN_SEARCH_API_TOKEN or GLEAN_INSTANCE in env.txt", file=sys.stderr)
    sys.exit(1)

# Create the MCP server
mcp = FastMCP("volta-coffee-chatbot")

# @mcp.tool() is required — it registers ask_volta so Claude Desktop can see and call it
@mcp.tool()
def ask_volta(question: str) -> str:
    """Ask a question about Volta Coffee Co. internal documentation."""
    result = rag_query(API_TOKEN, INSTANCE, question)
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    mcp.run(transport="stdio")
