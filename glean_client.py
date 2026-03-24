from glean.api_client import Glean


def glean_search(api_token, instance, query, page_size=5, act_as_email=""):
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
            http_headers={"X-Glean-ActAs": act_as_email},
        )
        if response.results:
            for item in response.results:
                doc = item.document

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
        else:
            results = []


    return results


def glean_chat(api_token, instance, question, timeout_millis=30000, act_as_email=""):
    # Send a question to Glean Chat and return the answer with sources
    server_url = f"https://{instance}-be.glean.com"

    with Glean(api_token=api_token, server_url=server_url) as client:
        response = client.client.chat.create(
            messages=[{
                "author": "USER",
                "fragments": [{"text": question}],
            }],
            timeout_millis=timeout_millis,
            http_headers={"X-Glean-ActAs": act_as_email},
        )

    # Build the answer text from the last assistant message only
    answer = ""
    if response.messages:
        last_assistant_msg = None
        for msg in response.messages:
            if msg.author.upper() != "USER":
                last_assistant_msg = msg
        if last_assistant_msg:
            for frag in (last_assistant_msg.fragments or []):
                if frag and frag.text:
                    answer += frag.text
    else:
        print("No messages found in the response.")

    # Pull out the cited source documents
    sources = []
    seen_ids = set()
    if response.messages:
        for msg in response.messages:
            if msg.author.upper() == "USER":
                continue
            for frag in (msg.fragments or []):
                cite = getattr(frag, "citation", None)
                if cite and cite.source_document:
                    doc = cite.source_document
                    doc_id = doc.id or ""
                    if doc_id not in seen_ids:
                        seen_ids.add(doc_id)
                        sources.append({
                            "title": doc.title or "",
                            "url": doc.url or "",
                            "doc_id": doc_id,
                        })

    return {"answer": answer, "sources": sources}




    