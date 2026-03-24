import json
import sys

from indexer import load_env, index_documents
from glean_client import glean_search, glean_chat

USAGE = """
Usage:
  python main.py index                    Index documents into Glean
  python main.py search "your query"      Test the Search API
  python main.py chat "your query"        Test the Chat API
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
    client_token = config.get("GLEAN_CLIENT_API_TOKEN", "")
    act_as_email = config.get("GLEAN_ACT_AS_EMAIL", "")
    instance = config.get("GLEAN_INSTANCE", "")

    if command == "index":
        index_documents(indexing_token, instance)
        return

    if not query:
        print(f"Usage: python main.py {command} \"your query\"")
        sys.exit(1)

    if command == "search":
        results = glean_search(client_token, instance, query,act_as_email=act_as_email)
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
        result = glean_chat(client_token, instance, query, act_as_email=act_as_email)
        print("\n=== Answer ===")
        print(result["answer"])
        if result["sources"]:
            print("\n=== Sources ===")
            for s in result["sources"]:
                print(f"  - {s['title']} ({s['url']})")
    else:
        print(f"Unknown command: {command}")
        print(USAGE)
        sys.exit(1)


if __name__ == "__main__":
    main()
