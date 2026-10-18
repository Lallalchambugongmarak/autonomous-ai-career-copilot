
from shared_state.plans import AgentPlan


VALID_AGENTS = {
    "research",
    "analysis",
    "retrieval",
    "verification",
    "synthesis",
    "automation",
}


def validate_agent_plan(plan: AgentPlan) -> bool:
    """Validate the objective and tasks in an agent plan."""

    if not plan.objective.strip():
        return False

    if not plan.tasks:
        return False

    for task in plan.tasks:
        if not task.task_id.strip():
            return False

        if not task.description.strip():
            return False

        if task.agent not in VALID_AGENTS:
            return False

    return True
