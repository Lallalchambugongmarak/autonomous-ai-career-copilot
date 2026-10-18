
import json

from google.genai import types


def generate_structured_response(
    prompt: str,
    response_model,
    client,
    model: str,
):
    """Generate and validate structured JSON using the Gemini API."""

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=response_model,
        ),
    )

    if response.text is None:
        raise RuntimeError("The model returned no structured response.")

    return response_model.model_validate(json.loads(response.text))
