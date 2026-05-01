from code.commands import COMMANDS
from code.commands.types import AnalysisResult
from code.config import DEFAULT_CONFIG

COMMAND_PREFIX = "/"

class Analyzer:
  def __init__(self, commands=None):
    self.commands = commands or COMMANDS

  def analyze(self, raw_input, config=DEFAULT_CONFIG):
    if raw_input.startswith(COMMAND_PREFIX):
      return self.analyze_command(raw_input, config)

    return AnalysisResult(kind="message", content=raw_input)

  def analyze_command(self, raw_input, config=DEFAULT_CONFIG):
    command_name, args = self.parse_command(raw_input)
    handler = self.commands.get(command_name)

    if handler is None:
      return AnalysisResult(
        kind="command",
        command=command_name,
        content=f"Unknown command: /{command_name}. Use /help to list available commands.",
      )

    return handler(args, config)

  def parse_command(self, raw_input):
    command_text = raw_input.removeprefix(COMMAND_PREFIX).strip()

    if not command_text:
      return "", ()

    command_name, *args = command_text.split()

    return command_name.lower(), tuple(args)

