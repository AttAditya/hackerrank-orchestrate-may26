from code.agents.dummy import DummyAgent
from code.agents.ollama import OllamaAgent

AGENTS = {
  "dummy": DummyAgent,
  "ollama": OllamaAgent,
}

def get_agent(provider):
  agent_class = AGENTS.get(provider, DummyAgent)

  return agent_class()

