from code.commands.types import AnalysisResult
from code.providers import get_provider

def handle(args, config):
  if not args:
    return AnalysisResult(
      kind="command",
      command="provider",
      content="\n".join(
        [
          f"Current provider: {config.provider}",
          "Available providers:",
          *format_providers(config),
        ]
      ),
    )

  requested_provider = args[0]

  if requested_provider not in config.available_providers():
    return AnalysisResult(
      kind="command",
      command="provider",
      content="\n".join(
        [
          f"Provider not changed. Unknown provider: {requested_provider}",
          "Available providers:",
          *format_providers(config),
        ]
      ),
    )

  config.provider = requested_provider
  provider = get_provider(config.provider)

  if not provider.has_model(config.model):
    config.model = provider.list_models()[0]

  config.save()

  return AnalysisResult(
    kind="command",
    command="provider",
    content="\n".join(
      [
        f"Provider changed to: {config.provider}",
        f"Current model: {config.model}",
      ]
    ),
  )

def format_providers(config):
  return [
    f"* {provider}"

    for provider in config.available_providers()
  ]

