class BaseIO:
  def read_input(self, prompt=""):
    raise NotImplementedError

  def write_output(self, message="", *, end="\n"):
    raise NotImplementedError

  def stream_output(self, chunks):
    raise NotImplementedError

