FALLBACK_MESSAGE = (
    "The approved customer success documents do not contain enough information "
    "to answer that question. Review the relevant policy or contact a supervisor "
    "before acting on this request."
)


def format_sources(context_chunks):
    """Return source metadata for retrieved context chunks."""
    # TODO: Return unique source dictionaries.
    # TODO: Include id, title, category, section, and chunk_id.
    # TODO: Do not include full text or distance values in source entries.
    if not context_chunks or not isinstance(context_chunks, list):
        return []

    seen_ids = set()
    sources = []

    for chunk in context_chunks:
        if not isinstance(chunk, dict):
            continue

        source_id = chunk.get("source_id")
        if not source_id or source_id in seen_ids:
            continue

        seen_ids.add(source_id)
        sources.append(
            {
                "id": source_id,
                "title": chunk.get("title", ""),
                "category": chunk.get("category", ""),
                "section": chunk.get("section", ""),
                "chunk_id": chunk.get("id", ""),
            }
        )

    return sources


def format_success_response(answer, sources):
    """Return the successful RAG API response body."""
    # TODO: Return {"answer": cleaned_answer, "sources": sources_list}.
    cleaned_answer = answer.strip() if isinstance(answer, str) else ""
    sources_list = list(sources) if sources else []

    return {
        "answer": cleaned_answer,
        "sources": sources_list,
    }


def format_fallback_response(question=None):
    """Return a safe response when there is not enough approved context."""
    # TODO: Return FALLBACK_MESSAGE with an empty sources list.
    return {
        "answer": FALLBACK_MESSAGE,
        "sources": [],
    }


def format_error_response(error, message):
    """Return a standard error response body."""
    # TODO: Return {"error": error, "message": message}.
    return {
        "error": error,
        "message": message,
    }