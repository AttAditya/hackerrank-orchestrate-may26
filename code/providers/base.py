class BaseModelProvider:
  name = "base"

  def list_models(self):
    raise NotImplementedError

  def has_model(self, model):
    return model in self.list_models()

