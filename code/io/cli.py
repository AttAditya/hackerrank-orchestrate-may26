from code.io.base import BaseIO

class CliIO(BaseIO):
  def read_input(self, prompt=""):
    return read_input(prompt)

  def write_output(self, message="", *, end="\n"):
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

