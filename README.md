# Volta Coffee Co. — Glean RAG Chatbot + MCP Tool

An enterprise chatbot prototype that indexes internal documentation into Glean and exposes a RAG-powered Q&A flow as both a CLI and an MCP tool for Claude Desktop.

## Architecture & Data Flow

```
  ┌──────────────────────────┐
  │    Volta Coffee Docs      │
  │    (markdown files)       │
  └────────────┬──────────────┘
               │
    ┌──────────▼──────────┐
    │  Glean Indexing API  │
    │  (document push via  │
    │   API client)        │
    └──────────┬──────────┘
               │
    Glean indexes, chunks,
    and embeds internally
               │
  ┌────────────┼────────────────┐
  │                             │
  ▼                             ▼
  CLI (main.py)           MCP server
  index / search / chat   (Claude Desktop)
  │                             │
  └──────────┬──────────────────┘
             │
             ▼
      glean_client.py
      glean_search() → Glean Search API
      glean_chat()   → Glean Chat API
```

### How a query flows

1. User sends a natural-language question via the CLI or through the `ask_volta` MCP tool in Claude Desktop.
2. `glean_chat()` sends the question to the Glean Chat API with `X-Glean-ActAs` set to the configured user email. The Chat API internally retrieves relevant documents from the index and generates a grounded answer.
3. The response is parsed to extract the final answer (filtering out intermediate reasoning steps) and deduplicated source citations.
4. A JSON object is returned containing the answer text and a sources array with title, URL, and document ID for each cited document.

The Search API is available as a standalone CLI command (`python main.py search`) for verifying that indexed content is discoverable. The Chat API performs its own internal retrieval, so the search step serves as an independent validation tool.

## Setup

### Prerequisites

- Python 3.10+
- A Glean sandbox instance with the `interviewds` datasource configured

### Install

```bash
pip install -r requirements.txt
```

### Configuration

Create an `env.txt` file with your credentials:

```
GLEAN_INSTANCE: support-lab
GLEAN_INDEXING_API_TOKEN: <your-indexing-token>
GLEAN_SEARCH_API_TOKEN: <your-search-token>
GLEAN_CLIENT_API_TOKEN: <your-client-token>
GLEAN_ACT_AS_EMAIL: <user-email-for-impersonation>
```

The Indexing API token is used for document ingestion. The Client API token (Global scope) is used for Search and Chat API calls, with `X-Glean-ActAs` set to the configured email for user impersonation.

## Usage

### Index documents

```bash
python main.py index
```

Reads all `.md` files from `documents/` and pushes them to Glean via the Indexing API.

### Test search

```bash
python main.py search "Which drinks at Volta are only available in 12oz?"
```

Queries the Glean Search API filtered to the `interviewds` datasource and returns ranked document snippets.

### Test chat

```bash
python main.py chat "Who came up with the coffee menu at Volta Coffee?"
```

Sends the question to the Glean Chat API and returns a grounded answer with source citations.

### MCP Server (Claude Desktop)

The MCP server exposes a single tool (`ask_volta`) that accepts a natural-language question and returns a grounded answer with sources.

Add the following to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "volta-coffee": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "<PATH_TO_DIR>"
    }
  }
}
```

Restart Claude Desktop after saving. The `ask_volta` tool will appear and can be invoked by asking any question about Volta Coffee Co.

## Assumptions & Tradeoffs

**Flat permissions model.** All documents are indexed with `allow_anonymous_access=True`. In production, the Indexing API's `DocumentPermissionsDefinition` would map to the customer's identity provider, enforcing per-document ACLs. Combined with the Global token's `X-Glean-ActAs` impersonation, this ensures search results and chat answers respect the authenticated user's permissions — the standard architecture for a server-side chatbot where a single service account handles requests on behalf of multiple users.

**Chat API handles retrieval internally.** The Glean Chat API performs its own search and retrieval before generating an answer. The explicit Search API call in the CLI is not passed as context to the Chat API — it exists to independently verify that documents are indexed and discoverable, and to demonstrate the Search API as a standalone capability. This means there are effectively two retrieval paths, which is redundant but intentional given the exercise requirement to use all three APIs.

**Chain-of-thought filtering.** The Chat API returns intermediate reasoning steps (tool searches, document reads, drafting notes) alongside the final answer. Only the last assistant message is extracted to produce a clean response. This is brittle — if Glean changes the response structure, the filtering logic would need to be updated.

