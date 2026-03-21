# Volta Coffee Co. — Glean RAG Chatbot + MCP Tool

An enterprise chatbot prototype that indexes internal documentation into Glean and exposes a RAG pipeline (Search + Chat) as both a CLI tool and an MCP server.

## Architecture & Data Flow

```
                  ┌──────────────────────────┐
                  │    Volta Coffee Docs      │
                  │    (10 markdown files)     │
                  └────────────┬───────────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Glean Indexing API  │
                    │  (bulk document     │
                    │   push via SDK)     │
                    └──────────┬──────────┘
                               │
                    Glean indexes, chunks,
                    and embeds internally
                               │
          ┌────────────────────┼────────────────┐
          │                    │                 │
  ┌───────▼────────┐  ┌───────▼────────┐       │
  │  CLI (main.py) │  │ MCP server     │       │
  │  ask / search  │  │ (Claude Desktop │       │
  │  / chat        │  │  or Cursor)    │       │
  └───────┬────────┘  └───────┬────────┘       │
          │                    │                 │
          └────────────────────┘                 │
                               │                 │
                    ┌──────────▼──────────┐      │
                    │   rag_query()       │      │
                    │   glean_client.py   │      │
                    └──────────┬──────────┘      │
                               │                 │
              ┌────────────────┼──────────┐      │
              │                           │      │
     ┌────────▼─────────┐     ┌───────────▼──────▼──┐
     │ Glean Search API │     │  Glean Chat API     │
     │ (ranked snippets)│     │  (grounded answer)  │
     └──────────────────┘     └─────────────────────┘
```

### Flow for a single query

1. **User** sends a natural-language question (via CLI or MCP tool in Claude Desktop/Cursor).
2. **glean_search()** — hits the Glean Search API filtered to the `interviewds` datasource, returns ranked document snippets.
3. **glean_chat()** — sends the same question to the Glean Chat API, which performs its own internal retrieval and generates a grounded answer with citations.
4. **Source merging** — citations from Chat are combined with Search results (deduplicated by doc ID) to provide comprehensive provenance.
5. **Response** — JSON object with `answer`, `sources[]` (each with title, URL, doc_id, origin).

## Setup

### Prerequisites

- Python 3.10+
- A Glean sandbox instance with the `interviewds` datasource configured

### Install

```bash
pip install -r requirements.txt
```

### Configuration

Edit `env.txt` with your credentials:

```
GLEAN_INSTANCE: support-lab
GLEAN_INDEXING_API_TOKEN: <your-indexing-token>
GLEAN_SEARCH_API_TOKEN: <your-search-token>
```

The Indexing API token is used for document ingestion. The Search API token is used for Search and Chat API calls (they share the Client API token).

## Usage

### Index documents

```bash
python main.py index
```

Reads all `.md` files from `documents/` and pushes them to Glean.

### Test search

```bash
python main.py search "espresso extraction parameters"
```

### Test chat

```bash
python main.py chat "What is the PTO policy for baristas?"
```

### Full RAG query (search + chat)

```bash
python main.py ask "How do I calibrate the espresso grinder?"
```

### MCP Server (for Claude Desktop / Cursor)

```bash
python mcp_server.py
```

Claude Desktop config (`%APPDATA%\Claude\claude_desktop_config.json` on Windows, `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):
```json
{
  "mcpServers": {
    "volta-coffee": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "/path/to/this/project"
    }
  }
}
```

Cursor config (`.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "volta-coffee": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "/path/to/this/project"
    }
  }
}
```

Restart the client after saving. The `ask_volta` tool will appear and can be invoked by asking any question about Volta Coffee Co.

## Assumptions

1. **Single datasource**: All documents target the `interviewds` datasource. In production, you'd use multiple datasources or object types to model different content categories.
2. **Flat permissions**: Documents are indexed with `allow_anonymous_access=True`. A real deployment would map to the customer's identity provider and enforce per-document ACLs.
3. **Chat API does its own retrieval**: The Glean Chat API performs internal search — we don't pass our Search results to it as context. The explicit Search step is included because the exercise requires using all three APIs, and it gives us deterministic source references we control.
4. **No chunking logic**: Glean handles chunking and embedding internally. We push full document bodies. This is a feature of Glean's managed pipeline, not an omission.
5. **env.txt for secrets**: Acceptable for a prototype. Production would use environment variables or a secrets manager.
6. **Synchronous SDK calls**: The Glean Python SDK supports async, but the MCP FastMCP `@mcp.tool()` decorator works with sync functions. For a production MCP server under load, you'd use the async client.

## File Structure

```
├── main.py              CLI entrypoint (index / search / chat / ask)
├── indexer.py           Document reader + Glean Indexing API client
├── glean_client.py      Glean Search + Chat API functions, RAG orchestration
├── mcp_server.py        MCP server (stdio transport for Claude Desktop / Cursor)
├── env.txt              Configuration (tokens, instance name)
├── requirements.txt     Python dependencies
├── documents/           Volta Coffee Co. internal docs (10 markdown files)
└── README.md            This file
```

## Key Tradeoffs & Limitations

| Decision | Tradeoff |
|----------|----------|
| Using Chat API for generation instead of a custom LLM | Less control over prompting, but answers are grounded in Glean's index by default — no prompt engineering needed for citation |
| Explicit search step alongside Chat | Redundant retrieval, but demonstrates the Search API independently and gives us controllable source references |
| Single MCP tool (`ask_volta`) | Simpler interface for the client; could be split into `search_volta` + `chat_volta` for more granular control |
| Synchronous Glean client in MCP | Simpler code; would bottleneck under concurrent requests — async client needed for production |
| stdio-only MCP transport | Simplest setup for local clients (Claude Desktop, Cursor); SSE or Streamable HTTP would be needed for remote/multi-client access |
