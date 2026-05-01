from code.commands.types import AnalysisResult

def handle(args, config):
  return AnalysisResult(
    kind="command",
    command="help",
    content="\n".join(
      [
        "Available commands:",
        *format_commands(),
      ]
    ),
  )

def format_commands():
  from code.commands.registry import COMMAND_DETAILS

  return [
    f"/{name} - {description}"

    for name, description in sorted(COMMAND_DETAILS.items())
  ]

