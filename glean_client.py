from glean.api_client import Glean


def glean_search(api_token, instance, query, page_size=5):
    # Search the Glean index and return a list of matching documents
    server_url = f"https://{instance}-be.glean.com"
    results = []

    with Glean(api_token=api_token, server_url=server_url) as client:
        response = client.client.search.query(
            query=query,
            page_size=page_size,
            request_options={
                "datasources_filter": ["interviewds"],
                "facet_bucket_size": 10,
            },
        )

        for item in getattr(response, "results", []) or []:
            doc = getattr(item, "document", None)

            snippets = getattr(item, "snippets", None) or []
            snippet_text = ""
            if snippets:
                first = snippets[0]
                snippet_text = getattr(first, "text", "") or getattr(first, "snippet", "") or ""

            results.append({
                "title": getattr(doc, "title", "") if doc else "",
                "url": getattr(doc, "url", "") if doc else "",
                "doc_id": getattr(doc, "id", "") if doc else "",
                "snippet": snippet_text,
            })

    return results


def glean_chat(api_token, instance, question, timeout_millis=30000):
    # Send a question to Glean Chat and return the answer with sources
    server_url = f"https://{instance}-be.glean.com"

    with Glean(api_token=api_token, server_url=server_url) as client:
        response = client.client.chat.create(
            messages=[{
                "author": "USER",
                "fragments": [{"text": question}],
            }],
            timeout_millis=timeout_millis,
        )

    # Build the answer text from the assistant's response fragments
    answer = ""
    for msg in getattr(response, "messages", []) or []:
        if getattr(msg, "author", "").upper() != "USER":
            for frag in getattr(msg, "fragments", []) or []:
                answer += getattr(frag, "text", "") or ""

    # Pull out the cited source documents
    sources = []
    for cite in getattr(response, "citations", []) or []:
        doc = getattr(cite, "source_document", None) or getattr(cite, "document", None)
        if doc:
            sources.append({
                "title": getattr(doc, "title", ""),
                "url": getattr(doc, "url", ""),
                "doc_id": getattr(doc, "id", ""),
            })

    return {"answer": answer, "sources": sources}


def rag_query(api_token, instance, question, top_k=5):
    # Run search and chat, then combine their sources into one list
    search_results = glean_search(api_token, instance, question, page_size=top_k)
    chat_result = glean_chat(api_token, instance, question)

    seen = set()
    sources = []

    for src in chat_result["sources"]:
        key = src["doc_id"] or src["url"]
        if key and key not in seen:
            seen.add(key)
            src["origin"] = "chat_citation"
            sources.append(src)

    for src in search_results:
        key = src["doc_id"] or src["url"]
        if key and key not in seen:
            seen.add(key)
            src["origin"] = "search"
            sources.append(src)

    return {
        "question": question,
        "answer": chat_result["answer"],
        "sources": sources,
    }
