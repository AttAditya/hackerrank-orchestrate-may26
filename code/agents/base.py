class BaseAgent:
  def respond(self, message, config, history=None):
    raise NotImplementedError

  def stream_respond(self, message, config, history=None):
    yield self.respond(message, config, history)

