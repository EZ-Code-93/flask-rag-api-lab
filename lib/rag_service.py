from lib.model_client import ModelClientError, generate_answer
from lib.prompt_builder import build_rag_prompt
from lib.response_formatter import (
    format_fallback_response,
    format_sources,
    format_success_response,
)
from lib.retrieval import DEFAULT_TOP_K, retrieve_context


def answer_question(
    question,
    retriever=None,
    prompt_builder=None,
    model_client=None,
    top_k=DEFAULT_TOP_K,
):
    """Run the full RAG workflow for a validated question."""
    # TODO: Use provided dependencies when passed, otherwise use default helpers.
    # TODO: Retrieve context before building the prompt.
    # TODO: Return fallback response and do not call the model when context is empty.
    # TODO: Build the prompt.
    # TODO: Call the model client.
    # TODO: Raise ModelClientError if the model answer is blank or unusable.
    # TODO: Return formatted success response with answer and sources.
    active_retriever = retriever if retriever is not None else retrieve_context
    active_prompt_builder = (
        prompt_builder if prompt_builder is not None else build_rag_prompt
    )
    active_model_client = (
        model_client if model_client is not None else generate_answer
    )

    context_chunks = active_retriever(question, top_k=top_k)

    if not context_chunks:
        return format_fallback_response(question)

    prompt = active_prompt_builder(question, context_chunks)
    raw_answer = active_model_client(prompt)

    if not isinstance(raw_answer, str) or not raw_answer.strip():
        raise ModelClientError("Model returned a blank or unusable answer.")

    sources = format_sources(context_chunks)
    return format_success_response(raw_answer, sources)