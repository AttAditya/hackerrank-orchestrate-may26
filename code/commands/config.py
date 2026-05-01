from code.commands.types import AnalysisResult

def handle(args, config):
  stream_status = "enabled" if config.use_stream else "disabled"

  return AnalysisResult(kind="command", command="config", content=f"stream: {stream_status}")

