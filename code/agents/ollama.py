import json

import urllib.request

from code.agents.base import BaseAgent

class OllamaAgent(BaseAgent):
  def respond(self, message, config):
    payload = {
      "model": config.model,
      "prompt": message,
      "stream": False
    }

    try:
      req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"}
      )

      with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())

        return result.get("response", "")
    except Exception as e:
      return f"Error connecting to Ollama: {str(e)}"

  def stream_respond(self, message, config):
    payload = {
      "model": config.model,
      "prompt": message,
      "stream": True
    }

    try:
      req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"}
      )

      with urllib.request.urlopen(req) as response:
        for line in response:
          chunk = json.loads(line.decode())

          if "response" in chunk:
            yield chunk["response"]

          if chunk.get("done"):
            break
    except Exception as e:
      yield f"Error connecting to Ollama: {str(e)}"

