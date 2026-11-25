import requests

DEFAULT_MODEL_NAME = "llama3.2"
DEFAULT_BASE_URL = "http://localhost:11434"


class ModelClientError(Exception):
    """Raised when the local model service cannot return a usable answer."""


def generate_answer(prompt, model_name=DEFAULT_MODEL_NAME, base_url=DEFAULT_BASE_URL):
    """Send the prompt to a local Ollama model and return the generated answer."""
    # TODO: Validate that prompt is a non-empty string.
    # TODO: POST to {base_url}/api/generate.
    # TODO: Send model, prompt, and stream=False as JSON.
    # TODO: Use a timeout.
    # TODO: Raise ModelClientError for request failures, bad JSON, or missing response.
    # TODO: Return the stripped response text.
    if not isinstance(prompt, str) or not prompt.strip():
        raise ModelClientError("Prompt must be a non-empty string.")

    try:
        response = requests.post(
            f"{base_url}/api/generate",
            json={"model": model_name, "prompt": prompt, "stream": False},
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        if "response" not in data:
            raise ModelClientError("Missing response in JSON.")
        return data["response"].strip()
    except (requests.RequestException, ValueError) as e:
        raise ModelClientError(f"Failed to generate answer: {e}")