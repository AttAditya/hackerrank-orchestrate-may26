from code.agents.base import BaseAgent

class DummyAgent(BaseAgent):
  def respond(self, message, config):
    return f"You said: {message}"

