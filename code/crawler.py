import os

import re

import urllib.request

from urllib.parse import urlparse, urljoin

class Crawler:
  def __init__(self, save_dir="saves/crawled"):
    self.save_dir = save_dir

  def _get_domain_folder(self, url):
    netloc = urlparse(url).netloc

    return netloc.replace(".", "-")

  def _extract_links(self, html, base_url):
    links = re.findall(r'href=["\'](https?://[^"\']+|/[^"\']+)["\']', html)
    domain = urlparse(base_url).netloc
    absolute_links = []

    for link in links:
      full_url = urljoin(base_url, link)

      if urlparse(full_url).netloc == domain:
        absolute_links.append(full_url)

    return list(set(absolute_links))

  def crawl(self, start_url, max_level=1):
    domain_folder = self._get_domain_folder(start_url)
    target_dir = os.path.join(self.save_dir, domain_folder)

    if not os.path.exists(target_dir):
      os.makedirs(target_dir)

    visited = set()
    results_count = 0
    queue = [(start_url, 0)]

    while queue:
      url, level = queue.pop(0)

      if url in visited or level > max_level:
        continue

      visited.add(url)

      try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

        with urllib.request.urlopen(req, timeout=5) as response:
          html = response.read().decode('utf-8', errors='ignore')
          filename = re.sub(r'[^a-zA-Z0-9]', '_', url.replace(f"http://{urlparse(url).netloc}", "").replace(f"https://{urlparse(url).netloc}", ""))

          if not filename:
            filename = "index"

          file_path = os.path.join(target_dir, f"{filename}.html")

          with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

          results_count += 1

          if level < max_level:
            links = self._extract_links(html, url)

            for link in links:
              if link not in visited:
                queue.append((link, level + 1))
      except Exception:
        continue

    return results_count, domain_folder

