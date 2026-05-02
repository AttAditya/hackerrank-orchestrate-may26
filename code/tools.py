import os
from pathlib import Path

CRAWLED_DIR = Path("saves/crawled")

def list_domains():
    """Lists all domains that have been crawled."""
    if not CRAWLED_DIR.exists():
        return "No domains crawled yet."
    
    domains = [d.name for d in CRAWLED_DIR.iterdir() if d.is_dir()]
    if not domains:
        return "No domains crawled yet."
    
    return "Crawled domains:\n" + "\n".join(domains)

def list_files_in_domain(domain):
    """Lists all crawled files for a specific domain."""
    domain_dir = CRAWLED_DIR / domain
    if not domain_dir.exists() or not domain_dir.is_dir():
        return f"Domain '{domain}' not found in crawled data."
    
    files = [f.name for f in domain_dir.rglob("*") if f.is_file()]
    if not files:
        return f"No files found for domain '{domain}'."
    
    return f"Files for {domain}:\n" + "\n".join(files)

def read_crawled_file(domain, filename):
    """Reads the content of a specific crawled file."""
    file_path = CRAWLED_DIR / domain / filename
    # Handle nested files by searching recursively if filename is just the name
    if not file_path.exists():
        # Try searching recursively
        matches = list(CRAWLED_DIR / domain).rglob(filename)
        if matches:
            file_path = matches[0]
        else:
            return f"File '{filename}' not found for domain '{domain}'."
    
    try:
        return file_path.read_text(encoding='utf-8')
    except Exception as e:
        return f"Error reading file {filename}: {str(e)}"

def get_available_tools():
    return {
        "list_domains": "Lists all crawled domains. Args: none",
        "list_files_in_domain": "Lists all files for a specific domain. Args: domain (str)",
        "read_crawled_file": "Reads content of a file. Args: domain (str), filename (str)"
    }
