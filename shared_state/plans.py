
from pydantic import BaseModel, Field

from shared_state.tasks import AgentTask


class AgentPlan(BaseModel):
    """Structured plan for completing a user objective."""

    objective: str = Field(
        description="The main objective of the user's request"
    )

    tasks: list[AgentTask] = Field(
        description="Ordered list of tasks required to complete the objective"
    )
