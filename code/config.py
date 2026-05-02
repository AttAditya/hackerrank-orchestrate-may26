import json

import os

from code.providers import DEFAULT_PROVIDER, PROVIDERS, get_provider

BOOTSTRAP_FILE = ".config_location"

class AppConfig:
  def __init__(
    self,
    use_stream=True,
    model=None,
    provider=DEFAULT_PROVIDER,
    path="saves/config.json",
    system_prompt="""You are a professional support triage agent. Your purpose is to resolve support tickets by analyzing them against the provided knowledge base.

For every ticket, you MUST provide your final answer as a valid JSON object with the following five keys:
1. "status": Either "replied" (if you can answer using the corpus) or "escalated" (if the case is high-risk, sensitive, requires human permissions, or is outside the provided corpus).
2. "product_area": The most relevant support category or domain area.
3. "response": A user-facing answer grounded strictly in the support corpus. If "status" is "escalated", this should be a polite message stating the issue is being escalated.
4. "justification": A concise explanation of why you chose the status and how you arrived at the response.
5. "request_type": Must be one of ["product_issue", "feature_request", "bug", "invalid"].

SOP:
- Use the available tools (list_domains, list_files_in_domain, read_crawled_file) to gather information.
- Base your response ONLY on the provided corpus. Do not hallucinate policies.
- Escalate high-risk cases (e.g., fraud, security vulnerabilities, identity theft, account access restoration for non-admins).
- If the company is 'None', infer the domain from the content.

Your final response MUST be a JSON object and nothing else.
""",
  ):
    self.use_stream = use_stream
    self.provider = provider
    self.path = path
    self.model = model or self._get_default_model()
    self.system_prompt = system_prompt

  def _get_default_model(self):
    provider = get_provider(self.provider)
    models = provider.list_models()

    return models[0] if models else "dummy"

  def get_provider(self):
    return get_provider(self.provider)

  def available_models(self):
    return self.get_provider().list_models()

  def available_providers(self):
    return list(PROVIDERS.keys())

  def save(self):
    # Ensure parent directory exists
    dir_name = os.path.dirname(self.path)

    if dir_name and not os.path.exists(dir_name):
      os.makedirs(dir_name)

    data = {
      "use_stream": self.use_stream,
      "model": self.model,
      "provider": self.provider,
      "path": self.path,
      "system_prompt": self.system_prompt,
    }

    with open(self.path, "w") as f:
      json.dump(data, f)

    # Update bootstrap pointer

    with open(BOOTSTRAP_FILE, "w") as f:
      f.write(self.path)

  @classmethod
  def load(cls):
    path = "saves/config.json"

    if os.path.exists(BOOTSTRAP_FILE):
      with open(BOOTSTRAP_FILE, "r") as f:
        path = f.read().strip()

    if os.path.exists(path):
      with open(path, "r") as f:
        data = json.load(f)

        return cls(**data)

    # Create default and save it immediately to disk in PWD
    config = cls(path=path)
    config.save()

    return config

DEFAULT_CONFIG = AppConfig.load()

