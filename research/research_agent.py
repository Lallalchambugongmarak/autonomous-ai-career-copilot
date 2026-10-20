"""Gemini-powered research draft specialist."""

from runtime.llm_service import LLMService
from runtime.config import config


def run_research_task(task, client) -> dict:
    """Generate a research draft for a task.

    This function does not perform web retrieval or independent fact-checking.
    Its output must be verified before being treated as confirmed research.
    """
    if not task.description.strip():
        raise ValueError("Research task description cannot be empty.")

    if task.agent not in {"research", "retrieval"}:
        raise ValueError(
            "Research specialist only accepts research or retrieval tasks."
        )

    prompt = f"""
You are a research specialist in an AI multi-agent platform.

Research task:
{task.description}

Instructions:
- Provide a clear, structured research draft.
- Separate established background knowledge from uncertainty.
- Do not invent citations, URLs, experiments, or source material.
- Explicitly state that claims requiring current information need verification.
- End with a short list of claims that a verification specialist should check.
"""

    service = LLMService(client=client, model=config.llm_model)
    draft = service.generate(prompt)

    return {
        "task_id": task.task_id,
        "agent": "research",
        "status": "draft_generated",
        "content": draft,
        "independently_verified": False,
    }
