from code.providers.dummy import DummyModelProvider

DEFAULT_PROVIDER = "dummy"
PROVIDERS = {
  "dummy": DummyModelProvider(),
}

def get_provider(name):
  return PROVIDERS.get(name, PROVIDERS[DEFAULT_PROVIDER])

