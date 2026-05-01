from code.commands.types import AnalysisResult

def handle(args, config):
  stream_status = "enabled" if config.use_stream else "disabled"

  return AnalysisResult(
    kind="command",
    command="config",
    content="\n".join(
      [
        f"stream: {stream_status}",
        f"model: {config.model}",
        f"provider: {config.provider}",
        f"available_providers: {', '.join(config.available_providers())}",
      ]
    ),
  )

