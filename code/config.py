import json

import os

from code.providers import DEFAULT_PROVIDER, PROVIDERS, get_provider

BOOTSTRAP_FILE = ".config_location"

class AppConfig:
  def __init__(
    self,
    use_stream=True,
    model=None,
    provider=DEFAULT_PROVIDER,
    path="saves/config.json",
  ):
    self.use_stream = use_stream
    self.provider = provider
    self.path = path
    self.model = model or self._get_default_model()

  def _get_default_model(self):
    provider = get_provider(self.provider)
    models = provider.list_models()

    return models[0] if models else "dummy"

  def get_provider(self):
    return get_provider(self.provider)

  def available_models(self):
    return self.get_provider().list_models()

  def available_providers(self):
    return list(PROVIDERS.keys())

  def save(self):
    # Ensure parent directory exists
    dir_name = os.path.dirname(self.path)

    if dir_name and not os.path.exists(dir_name):
      os.makedirs(dir_name)

    data = {
      "use_stream": self.use_stream,
      "model": self.model,
      "provider": self.provider,
      "path": self.path,
    }

    with open(self.path, "w") as f:
      json.dump(data, f)

    # Update bootstrap pointer

    with open(BOOTSTRAP_FILE, "w") as f:
      f.write(self.path)

  @classmethod
  def load(cls):
    path = "saves/config.json"

    if os.path.exists(BOOTSTRAP_FILE):
      with open(BOOTSTRAP_FILE, "r") as f:
        path = f.read().strip()

    if os.path.exists(path):
      with open(path, "r") as f:
        data = json.load(f)

        return cls(**data)

    # Create default and save it immediately to disk in PWD
    config = cls(path=path)
    config.save()

    return config

DEFAULT_CONFIG = AppConfig.load()

