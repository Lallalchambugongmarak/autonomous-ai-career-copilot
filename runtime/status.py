def get_project_status(config, llm_connected: bool = False) -> dict:
    """Return the current project configuration and LLM status."""
    return {
        "project": config.project_name,
        "version": config.version,
        "environment": config.environment,
        "llm_provider": config.llm_provider,
        "llm_model": config.llm_model,
        "llm_connected": llm_connected,
    }


def print_project_status(config, llm_connected: bool = False) -> None:
    """Print the current project status."""
    project_status = get_project_status(config, llm_connected)

    for key, value in project_status.items():
        print(f"{key}: {value}")
