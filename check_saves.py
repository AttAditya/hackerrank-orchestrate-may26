import os
import re

def check_html_files(save_dir="saves/crawled"):
    bad_files = []
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
                    
                    # Check for empty or tiny files
                    if len(content) < 100:
                        bad_files.append((file_path, "Too small/Empty"))
                        continue
                    
                    # Check for basic HTML structure
                    if not re.search(r'<html', content, re.I) and not re.search(r'<body', content, re.I):
                        # It might be a CSS or JS file that the crawler saved as .html
                        if "content-type" in content.lower() and "text/css" in content.lower():
                            bad_files.append((file_path, "Actually CSS"))
                        elif "{" in content[:100] and "}" in content[-100:]:
                            bad_files.append((file_path, "Likely JSON/JS"))
                        else:
                            bad_files.append((file_path, "Missing HTML tags"))
                            
            except Exception as e:
                bad_files.append((file_path, f"Read error: {str(e)}"))
                
    return total_files, bad_files

if __name__ == "__main__":
    total, bad = check_html_files()
    print(f"Analyzed {total} files.")
    if bad:
        print(f"Found {len(bad)} problematic files:")
        for path, reason in bad:
            print(f"[{reason}] {path}")
    else:
        print("All files look like valid HTML!")
