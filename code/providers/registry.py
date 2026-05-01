from code.providers.dummy import DummyModelProvider
from code.providers.ollama import OllamaModelProvider

DEFAULT_PROVIDER = "dummy"
PROVIDERS = {
  "dummy": DummyModelProvider(),
  "ollama": OllamaModelProvider(),
}

def get_provider(name):
  return PROVIDERS.get(name, PROVIDERS[DEFAULT_PROVIDER])

