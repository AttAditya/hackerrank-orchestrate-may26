from code.providers import DEFAULT_PROVIDER, PROVIDERS, get_provider

class AppConfig:
  def __init__(
    self,
    use_stream=True,
    model="dummy",
    provider=DEFAULT_PROVIDER,
  ):
    self.use_stream = use_stream
    self.model = model
    self.provider = provider

  def get_provider(self):
    return get_provider(self.provider)

  def available_models(self):
    return self.get_provider().list_models()

  def available_providers(self):
    return list(PROVIDERS.keys())

DEFAULT_CONFIG = AppConfig()

