import json

import urllib.request

from code.providers.base import BaseModelProvider

class OllamaModelProvider(BaseModelProvider):
  name = "ollama"

  def list_models(self):
    try:
      with urllib.request.urlopen("http://localhost:11434/api/tags") as response:
        data = json.loads(response.read().decode())

        return [model["name"] for model in data.get("models", [])]
    except Exception:
      return []

