from code.providers.base import BaseModelProvider

class DummyModelProvider(BaseModelProvider):
  name = "dummy"

  def list_models(self):
    return ["dummy"]

