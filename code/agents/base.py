class BaseAgent:
  def respond(self, message, config):
    raise NotImplementedError

  def stream_respond(self, message, config):
    yield self.respond(message, config)

