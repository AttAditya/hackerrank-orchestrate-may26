from code.commands.types import AnalysisResult

def handle(args, config):
  provider = config.get_provider()

  if not args:
    return AnalysisResult(
      kind="command",
      command="model",
      content="\n".join(
        [
          f"Current model: {config.model}",
          f"Provider: {provider.name}",
          "Available models:",
          *format_models(provider),
        ]
      ),
    )

  requested_model = args[0]

  if not provider.has_model(requested_model):
    return AnalysisResult(
      kind="command",
      command="model",
      content="\n".join(
        [
          f"Model not changed. Unknown model for provider {provider.name}: {requested_model}",
          "Available models:",
          *format_models(provider),
        ]
      ),
    )

  config.model = requested_model

  return AnalysisResult(
    kind="command",
    command="model",
    content=f"Model changed to: {config.model} using provider: {provider.name}",
  )

def format_models(provider):
  return [
    f"* {model}"

    for model in provider.list_models()
  ]

