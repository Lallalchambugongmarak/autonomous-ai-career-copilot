
from shared_state.plans import AgentPlan
from runtime.config import config
from runtime.structured_output import generate_structured_response


def create_agent_plan(user_request: str, client) -> AgentPlan:
    """Convert a user request into an ordered multi-agent plan."""

    prompt = f"""
You are the Orchestrator Agent in an AI multi-agent system.

Break the user's request into clear, ordered tasks and assign
each task to the appropriate specialized agent.

Available agents:
- research
- analysis
- retrieval
- verification
- synthesis
- automation

Rules:
1. Do not perform the tasks yourself.
2. Assign each task to the most appropriate agent.
3. Keep the plan focused on the user's objective.
4. Order tasks logically.
5. Use verification before final synthesis when factual claims
   or external evidence are involved.
6. Use automation only when an actual external action is required.

User request:
{user_request}
"""

    return generate_structured_response(
        prompt=prompt,
        response_model=AgentPlan,
        client=client,
        model=config.llm_model,
    )
