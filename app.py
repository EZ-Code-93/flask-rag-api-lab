from flask import Flask, jsonify, request

from lib.model_client import ModelClientError
from lib.rag_service import answer_question
from lib.validation import validate_question_payload
from lib.response_formatter import format_error_response


def create_app():
    app = Flask(__name__)

    @app.post("/api/ask")
    def ask():
        # TODO: Read the JSON request body with request.get_json(silent=True).
        # TODO: Validate the payload with validate_question_payload().
        # TODO: Return a 400 JSON response for invalid input.
        # TODO: Call answer_question(question) for valid input.
        # TODO: Return a 502 JSON response for ModelClientError.
        # TODO: Return the RAG result as JSON with a 200 status code.
        payload = request.get_json(silent=True)

        question, error = validate_question_payload(payload)
        if error is not None:
            return jsonify(error), 400

        try:
            result = answer_question(question)
        except ModelClientError as exc:
            error_body = format_error_response(
                "model_service_error",
                str(exc) or "Failed to generate an answer from the model.",
            )
            return jsonify(error_body), 502

        return jsonify(result), 200

    return app


app = create_app()