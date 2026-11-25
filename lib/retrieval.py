CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "customer_success_knowledge"
DEFAULT_TOP_K = 3


def get_chroma_collection(path=CHROMA_PATH, collection_name=COLLECTION_NAME):
    """Return a persistent Chroma collection for manual local testing."""
    # TODO: Import chromadb inside this function.
    # TODO: Create a PersistentClient using path.
    # TODO: Return get_or_create_collection(collection_name).
    import chromadb

    client = chromadb.PersistentClient(path=path)
    return client.get_or_create_collection(collection_name)


def format_chroma_results(results):
    """Normalize Chroma query results into context chunk dictionaries.

    Chroma query results often look like:
        {
            "ids": [["chunk-1"]],
            "documents": [["Text"]],
            "metadatas": [[{"source_id": "SRC-1"}]],
            "distances": [[0.12]]
        }
    """
    # TODO: Handle nested Chroma result lists.
    # TODO: Skip missing or blank documents.
    # TODO: Return dictionaries with id, text, source_id, title, category,
    #       section, and distance keys.
    if not results or not isinstance(results, dict):
        return []

    ids_batch = results.get("ids") or [[]]
    documents_batch = results.get("documents") or [[]]
    metadatas_batch = results.get("metadatas") or [[]]
    distances_batch = results.get("distances") or [[]]

    ids = ids_batch[0] if ids_batch else []
    documents = documents_batch[0] if documents_batch else []
    metadatas = metadatas_batch[0] if metadatas_batch else []
    distances = distances_batch[0] if distances_batch else []

    formatted_chunks = []

    for index, doc in enumerate(documents):
        if not isinstance(doc, str) or not doc.strip():
            continue

        chunk_id = ids[index] if index < len(ids) else None
        metadata = metadatas[index] if index < len(metadatas) and metadatas[index] else {}
        distance = distances[index] if index < len(distances) else None

        formatted_chunks.append(
            {
                "id": chunk_id,
                "text": doc,
                "source_id": metadata.get("source_id", ""),
                "title": metadata.get("title", ""),
                "category": metadata.get("category", ""),
                "section": metadata.get("section", ""),
                "distance": distance,
            }
        )

    return formatted_chunks


def retrieve_context(question, collection=None, top_k=DEFAULT_TOP_K):
    """Retrieve context chunks for a user question.

    Tests may pass a fake collection. Manual use should call Chroma.
    """
    # TODO: Strip the question.
    # TODO: Use the provided collection or get_chroma_collection().
    # TODO: Call collection.query() with query_texts, n_results, and include.
    # TODO: Return normalized context chunks.
    if not isinstance(question, str):
        return []

    cleaned_question = question.strip()
    if not cleaned_question:
        return []

    active_collection = collection if collection is not None else get_chroma_collection()

    results = active_collection.query(
        query_texts=[cleaned_question],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    return format_chroma_results(results)