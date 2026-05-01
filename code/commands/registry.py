from code.commands import config, exit as exit_command, help, model, provider

COMMAND_DETAILS = {
  "config": "Show current application configuration.",
  "exit": "Exit the application.",
  "help": "List available commands.",
  "model": "Show or change the active model.",
  "provider": "Show or change the active model provider.",
}

COMMANDS = {
  "config": config.handle,
  "exit": exit_command.handle,
  "help": help.handle,
  "model": model.handle,
  "provider": provider.handle,
}

