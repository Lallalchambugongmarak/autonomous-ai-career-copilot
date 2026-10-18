
from shared_state.results import OrchestratorResult
from orchestration.planner import create_agent_plan
from orchestration.validation import validate_agent_plan


def run_orchestrator(user_request: str, client) -> OrchestratorResult:
    """Create a plan, validate it, and return the orchestration result."""

    plan = create_agent_plan(user_request, client)
    is_valid = validate_agent_plan(plan)

    return OrchestratorResult(
        objective=plan.objective,
        tasks=plan.tasks,
        valid=is_valid,
        task_count=len(plan.tasks),
    )
