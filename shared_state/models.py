
from pydantic import BaseModel, Field


class AgentResponse(BaseModel):
    """Structured response returned by an AI agent."""

    task: str = Field(description="The task given to the agent")
    summary: str = Field(description="The agent's concise response")
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1",
    )
