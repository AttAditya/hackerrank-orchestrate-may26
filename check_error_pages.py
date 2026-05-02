import os
import re

def check_for_error_pages(save_dir="saves/crawled"):
    error_patterns = {
        "404 Not Found": r"404\s*not\s*found",
        "403 Forbidden": r"403\s*forbidden",
        "500 Internal Server Error": r"500\s*internal\s*server\s*error",
        "Access Denied": r"access\s*denied",
        "Cloudflare/Captcha": r"cloudflare|captcha|ray-id|challenge-page",
        "Empty/Too Short": None # Handled by length
    }
    
    results = []
    total_files = 0
    
    for root, _, files in os.walk(save_dir):
        for file in files:
            if not file.endswith(".html"):
                continue
            
            total_files += 1
            file_path = os.path.join(root, file)
            
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    
                    if len(content) < 200:
                        results.append((file_path, "Too short/possible empty response"))
                        continue
                    
                    # Check for common error markers in title or body
                    for error_name, pattern in error_patterns.items():
                        if pattern and re.search(pattern, content, re.I):
                            results.append((file_path, error_name))
                            break
                            
            except Exception as e:
                results.append((file_path, f"Read error: {str(e)}"))
                
    return total_files, results

if __name__ == "__main__":
    total, errors = check_for_error_pages()
    print(f"Analyzed {total} files.")
    if errors:
        print(f"Found {len(errors)} suspected error pages:")
        for path, reason in errors:
            print(f"[{reason}] {path}")
    else:
        print("No obviously 'bad' error pages found!")
