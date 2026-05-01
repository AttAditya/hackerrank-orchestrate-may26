class AnalysisResult:
  def __init__(self, kind, content, command=None, should_exit=False):
    self.kind = kind
    self.content = content
    self.command = command
    self.should_exit = should_exit

  def __repr__(self):
    return (
      "AnalysisResult("
      f"kind={self.kind!r}, "
      f"content={self.content!r}, "
      f"command={self.command!r}, "
      f"should_exit={self.should_exit!r}"
      ")"
    )

