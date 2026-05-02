import json

import urllib.request

from code.agents.base import BaseAgent

class OllamaAgent(BaseAgent):
  def respond(self, message, config, history=None):
    messages = [{"role": "system", "content": config.system_prompt}]
    
    if history:
      messages.extend(history)
    
    messages.append({"role": "user", "content": message})

    payload = {
      "model": config.model,
      "messages": messages,
      "stream": False
    }

    try:
      req = urllib.request.Request(
        "http://localhost:11434/api/chat",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"}
      )

      with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())

        return result.get("message", {}).get("content", "")
    except Exception as e:
      return f"Error connecting to Ollama: {str(e)}"

  def stream_respond(self, message, config, history=None):
    messages = [{"role": "system", "content": config.system_prompt}]
    
    if history:
      messages.extend(history)
    
    messages.append({"role": "user", "content": message})

    payload = {
      "model": config.model,
      "messages": messages,
      "stream": True
    }

    try:
      req = urllib.request.Request(
        "http://localhost:11434/api/chat",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"}
      )

      with urllib.request.urlopen(req) as response:
        for line in response:
          chunk = json.loads(line.decode())

          if "message" in chunk:
            yield chunk["message"].get("content", "")

          if chunk.get("done"):
            break
    except Exception as e:
      yield f"Error connecting to Ollama: {str(e)}"

