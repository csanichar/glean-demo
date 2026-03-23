from glean.api_client import Glean


def glean_search(api_token, instance, query, page_size=5):
    # Search the Glean index and return a list of matching documents
    server_url = f"https://{instance}-be.glean.com"
    results = []

    with Glean(api_token=api_token, server_url=server_url) as client:
        response = client.client.search.query(
            query=query,
            page_size=page_size,
            request_options  ={
                "datasources_filter": ["interviewds"],
                "facet_bucket_size": 10,
            },
        )

        for item in getattr(response, "results", []) or []:
            doc = getattr(item, "document", None)

            #snippets = getattr(item, "snippets", None) or []
            snippets = item.snippets
            snippet_text = ""
            if snippets:
                first = snippets[0]
                snippet_text = first.text or first.snippet or ""

            results.append({
                "title": doc.title or "",
                "url": doc.url or  "",
                "doc_id": doc.id or "",
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
    if response.messages:
        for msg in response.messages: 
            if msg.author.upper() != "USER":
                for frag in msg.fragments:
                    if frag and frag.text: 
                        answer += frag.text
    else:
        print("No messages found in the response.")

    # Pull out the cited source documents
    sources = []
    if response.messages:
        for msg in response.messages:
            if msg.citations:
                for cite in msg.citations:
                    if cite.source_document:
                        sources.append({
                            "title": cite.source_document.title or "",
                            "url": cite.source_document.url or "",
                            "doc_id": cite.source_document.id or "",
                        })

    return {"answer": answer, "sources": sources}


def rag_query(api_token, instance, question, top_k=5):
    # Run search and chat, then combine their sources into one list
    search_results = glean_search(api_token, instance, question, page_size=top_k)
    chat_result = glean_chat(api_token, instance, question)


    return {
        "question": question,
        "answer": chat_result["answer"],
        "search_results": search_results,
    }
