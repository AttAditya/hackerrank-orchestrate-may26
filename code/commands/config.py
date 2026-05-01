import os

from code.commands.types import AnalysisResult

def handle(args, config):
  if args and args[0] == "use":
    if len(args) < 2:
      return AnalysisResult(
        kind="command",
        command="config",
        content="Usage: /config use <filepath>",
      )

    new_path = args[1]

    if os.path.isdir(new_path):
      new_path = os.path.join(new_path, "config.json")

    config.path = new_path
    config.save()

    return AnalysisResult(
      kind="command",
      command="config",
      content=f"Config path updated to: {config.path}",
    )

  stream_status = "enabled" if config.use_stream else "disabled"

  return AnalysisResult(
    kind="command",
    command="config",
    content="\n".join(
      [
        f"stream: {stream_status}",
        f"model: {config.model}",
        f"provider: {config.provider}",
        f"path: {config.path}",
        f"available_providers: {', '.join(config.available_providers())}",
      ]
    ),
  )

