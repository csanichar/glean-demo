import json
import sys

from indexer import load_env, index_documents
from glean_client import glean_search, glean_chat, rag_query

USAGE = """
Usage:
  python main.py index                    Index documents into Glean
  python main.py search "your query"      Test the Search API
  python main.py chat "your query"        Test the Chat API
  python main.py ask "your query"         Full RAG pipeline (search + chat)
"""


def main():
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(1)

    config = load_env("env.txt")
    command = sys.argv[1].lower()
    query = " ".join(sys.argv[2:])

    indexing_token = config.get("GLEAN_INDEXING_API_TOKEN", "")
    search_token = config.get("GLEAN_SEARCH_API_TOKEN", "")
    instance = config.get("GLEAN_INSTANCE", "")

    if command == "index":
        index_documents(indexing_token, instance)
        return

    if not query:
        print(f"Usage: python main.py {command} \"your query\"")
        sys.exit(1)

    if command == "search":
        results = glean_search(search_token, instance, query)
        if not results:
            print("No results found.")
            return
        for i, r in enumerate(results, 1):
            print(f"\n--- Result {i} ---")
            print(f"  Title:   {r['title']}")
            print(f"  Doc ID:  {r['doc_id']}")
            print(f"  URL:     {r['url']}")
            print(f"  Snippet: {r['snippet'][:200]}")

    elif command == "chat":
        result = glean_chat(search_token, instance, query)
        print("\n=== Answer ===")
        print(result["answer"])
        if result["sources"]:
            print("\n=== Sources ===")
            for s in result["sources"]:
                print(f"  - {s['title']} ({s['url']})")

    elif command == "ask":
        result = rag_query(search_token, instance, query)
        print("\n=== Answer ===")
        print(result["answer"])
        print("\n=== Sources ===")
        for s in result["search_results"]:
            print(f"{s['title']}")
            if s.get("url"):
                print(f"           {s['url']}")
        print("\n=== Raw JSON ===")
        print(json.dumps(result, indent=2))

    else:
        print(f"Unknown command: {command}")
        print(USAGE)
        sys.exit(1)


if __name__ == "__main__":
    main()
