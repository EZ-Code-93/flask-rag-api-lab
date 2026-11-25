def format_context_chunk(chunk):
    """Format one retrieved chunk for the prompt context block."""
    # TODO: Include source_id, title, category, section, and text.
    if not isinstance(chunk, dict):
        return ""

    text = chunk.get("text", "")
    if not isinstance(text, str) or not text.strip():
        return ""

    source_id = chunk.get("source_id", "")
    title = chunk.get("title", "")
    category = chunk.get("category", "")
    section = chunk.get("section", "")

    return (
        f"Source ID: {source_id}\n"
        f"Title: {title}\n"
        f"Category: {category}\n"
        f"Section: {section}\n"
        f"Content: {text.strip()}"
    )


def build_rag_prompt(question, context_chunks):
    """Build a structured RAG prompt from a question and retrieved context."""
    # TODO: Validate that the question is not blank.
    # TODO: Validate that context_chunks contains usable text.
    # TODO: Build a prompt with these sections:
    #       Instructions:
    #       Context:
    #       Question:
    #       Response Requirements:
    # TODO: Tell the model to use only approved context and avoid unsupported claims.
    if not isinstance(question, str) or not question.strip():
        raise ValueError("Question cannot be blank.")

    if not context_chunks or not isinstance(context_chunks, list):
        raise ValueError("Context chunks must contain usable text.")

    formatted_chunks = [
        formatted
        for chunk in context_chunks
        if (formatted := format_context_chunk(chunk))
    ]

    if not formatted_chunks:
        raise ValueError("Context chunks must contain usable text.")

    context_block = "\n\n---\n\n".join(formatted_chunks)
    cleaned_question = question.strip()

    return (
        "Instructions:\n"
        "Use only the approved context provided below to answer the customer support question. "
        "Do not invent facts, policies, or unsupported claims outside the approved context. "
        "If the approved context does not contain enough information to answer the question, "
        "state that clearly.\n\n"
        "Context:\n"
        f"{context_block}\n\n"
        "Question:\n"
        f"{cleaned_question}\n\n"
        "Response Requirements:\n"
        "- Base your answer strictly on the approved context.\n"
        "- Cite the relevant source IDs from the context.\n"
        "- Keep the response clear, accurate, and concise."
    )