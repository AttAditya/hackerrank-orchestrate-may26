from code.commands.types import AnalysisResult

def handle(args, config):
  return AnalysisResult(
    kind="command",
    command="exit",
    content="Goodbye.",
    should_exit=True,
  )

