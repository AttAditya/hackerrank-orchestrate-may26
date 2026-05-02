import json
from code.io.base import BaseIO

class CliIO(BaseIO):
  def read_input(self, prompt=""):
    return read_input(prompt)

  def write_output(self, message="", *, end="\n"):
    # Try to parse as JSON to only show the 'response' field to the user
    try:
      start = message.find('{')
      json_end = message.rfind('}') + 1
      if start != -1 and json_end != 0:
        json_str = message[start:json_end]
        data = json.loads(json_str)
        if "response" in data:
          message = data["response"]
    except Exception:
      pass # Fallback to original message if parsing fails
    
    write_output(message, end=end)

  def stream_output(self, chunks):
    stream_output(chunks)

def read_input(prompt=""):

  return input(prompt)

def write_output(message="", *, end="\n", stream=None):
  print(message, end=end, file=stream, flush=True)

def stream_output(chunks, *, stream=None):
  for chunk in chunks:
    print(chunk, end="", file=stream, flush=True)

