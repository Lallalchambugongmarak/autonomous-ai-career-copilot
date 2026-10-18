
from typing import Literal

from pydantic import BaseModel, Field


class AgentTask(BaseModel):
    """Structured task assigned to an agent."""

    task_id: str = Field(
        description="Unique identifier for the task"
    )

    description: str = Field(
        description="What the agent needs to accomplish"
    )

    agent: Literal[
        "research",
        "analysis",
        "retrieval",
        "verification",
        "synthesis",
        "automation",
    ] = Field(
        description="Agent responsible for the task"
    )

    priority: Literal["low", "medium", "high"] = Field(
        default="medium",
        description="Task priority",
    )
