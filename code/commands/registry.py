from code.commands import config, exit as exit_command, help

COMMAND_DETAILS = {
  "config": "Show current application configuration.",
  "exit": "Exit the application.",
  "help": "List available commands.",
}

COMMANDS = {
  "config": config.handle,
  "exit": exit_command.handle,
  "help": help.handle,
}

