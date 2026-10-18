
from pydantic import BaseModel

from shared_state.tasks import AgentTask


class OrchestratorResult(BaseModel):
    """Result returned after an agent plan is validated."""

    objective: str
    tasks: list[AgentTask]
    valid: bool
    task_count: int
