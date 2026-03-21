import os
import glob

from glean.api_client import Glean, models


def load_env(filepath="env.txt"):
    """Read key: value pairs from env.txt and return them as a dictionary."""
    config = {}
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if ": " in line:
                key, value = line.split(": ", 1)
                config[key.strip()] = value.strip()
    return config


def read_documents(folder="documents"):
    """
    Scan the folder for .md files and return a list of document dicts.
    Each dict has: id, title, and content.
    """
    documents = []

    for filepath in sorted(glob.glob(os.path.join(folder, "*.md"))):
        filename = os.path.basename(filepath)
        doc_id = os.path.splitext(filename)[0]  # e.g. "04_it_security"

        with open(filepath, encoding="utf-8") as f:
            content = f.read()

        # Use the first # heading as the title, fall back to the filename if none found
        title = doc_id
        for line in content.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break

        documents.append({
            "id": doc_id,
            "title": title,
            "content": content,
        })

    return documents


def index_documents(api_token, instance):
    """Connect to Glean and index all documents found in the documents folder."""
    server_url = f"https://{instance}-be.glean.com"
    documents = read_documents()

    print(f"Found {len(documents)} document(s) to index.")
    print(f"Connecting to: {server_url}\n")

    # Build a list of DocumentDefinition objects from our local files
    glean_docs = []
    for doc in documents:
        glean_docs.append(
            models.DocumentDefinition(
                datasource="interviewds",
                object_type="KnowledgeArticle",
                id=doc["id"],
                title=doc["title"],
                view_url=f"https://{instance}.glean.com/kb/{doc['id']}",
                body=models.ContentDefinition(
                    mime_type="text/plain",
                    text_content=doc["content"],
                ),
                permissions=models.DocumentPermissionsDefinition(
                    allow_anonymous_access=True,
                ),
            )
        )

    with Glean(api_token=api_token, server_url=server_url) as client:
        print(f"Sending {len(glean_docs)} document(s) to Glean...")
        try:
            client.indexing.documents.index(
                datasource="interviewds",
                documents=glean_docs,
            )
            print("  -> Success")
        except Exception as e:
            print(f"  -> Failed: {e}")
