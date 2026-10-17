
class LLMService:
    """Service for generating text with the configured Gemini model."""

    def __init__(self, client, model: str):
        self.client = client
        self.model = model

    def generate(self, prompt: str) -> str:
        """Generate text from a prompt."""
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        if response.text is None:
            raise RuntimeError(
                "The model returned no text response."
            )

        return response.text
