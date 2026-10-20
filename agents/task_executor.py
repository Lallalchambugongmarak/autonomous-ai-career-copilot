"""Task dispatch foundation for the multi-agent platform."""

from shared_state.tasks import AgentTask

SUPPORTED_AGENTS = {
    "research",
    "analysis",
    "retrieval",
    "verification",
    "synthesis",
    "automation",
}


def validate_task_for_execution(task: AgentTask) -> bool:
    """Check whether a task has enough information to be dispatched."""
    if not task.task_id.strip():
        return False

    if not task.description.strip():
        return False

    if task.agent not in SUPPORTED_AGENTS:
        return False

    return True


def prepare_task_dispatch(task: AgentTask) -> dict:
    """Prepare a task for dispatch without claiming it was executed."""
    if not validate_task_for_execution(task):
        raise ValueError("Task is invalid or uses an unsupported agent.")

    return {
        "task_id": task.task_id,
        "agent": task.agent,
        "priority": task.priority,
        "description": task.description,
        "status": "ready",
    }
