from dataclasses import dataclass


@dataclass
class ProjectConfig:
    project_name: str = "AI Multi-Agent Research & Automation Platform"
    version: str = "0.1.0"
    environment: str = "development"
    llm_provider: str = "google"
    llm_model: str = "gemini-3.5-flash-lite"

config = ProjectConfig()

print("Project:", config.project_name)
print("Version:", config.version)
print("Environment:", config.environment)
print("LLM Provider:", config.llm_provider)
print("LLM Model:", config.llm_model)
