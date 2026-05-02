from code.commands.types import AnalysisResult
from code.crawler import Crawler

def handle(args, config):
  if len(args) < 2:
    return AnalysisResult(
      kind="command",
      command="crawl",
      content="Usage: /crawl <url> <nesting-level>",
    )

  url = args[0]

  try:
    level = int(args[1])
  except (ValueError, IndexError):
    return AnalysisResult(
      kind="command",
      command="crawl",
      content="Error: Nesting level must be an integer.",
    )

  crawler = Crawler()
  count, domain = crawler.crawl(url, level)

  return AnalysisResult(
    kind="command",
    command="crawl",
    content=f"Crawl complete. Saved {count} pages from {domain} to saves/crawled/{domain}/",
  )

