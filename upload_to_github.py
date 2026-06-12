import os
import base64
import requests
import sys

# GitHub 配置
REPO_OWNER = "LuoHong2000"
REPO_NAME = "1111"
REPO_URL = f"https://github.com/{REPO_OWNER}/{REPO_NAME}.git"

# 需要忽略的文件/目录
IGNORE_PATTERNS = [
    ".git", "__pycache__", "chroma_db", "chroma_db_new", "venv", "env",
    ".vscode", ".idea", "*.pyc", "*.pyo", "*.pyd", ".DS_Store", "Thumbs.db",
    "*.log", "AI_USAGE_LOG.md", "*.sqlite", "*.sqlite3"
]

def should_ignore(path):
    basename = os.path.basename(path)
    for pattern in IGNORE_PATTERNS:
        if pattern.startswith("*."):
            if basename.endswith(pattern[1:]):
                return True
        elif basename == pattern:
            return True
    return False

def get_all_files(root_dir):
    files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not should_ignore(d)]
        
        for filename in filenames:
            if should_ignore(filename):
                continue
            
            filepath = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(filepath, root_dir)
            files.append((rel_path, filepath))
    
    return files

def upload_files(token):
    root_dir = os.getcwd()
    files = get_all_files(root_dir)
    
    if not files:
        print("ERROR: No files to upload")
        return False
    
    print("INFO: Found %d files to upload" % len(files))
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    success_count = 0
    fail_count = 0
    
    for rel_path, filepath in files:
        print("Uploading: %s..." % rel_path)
        
        try:
            with open(filepath, "rb") as f:
                content = f.read()
            
            encoded_content = base64.b64encode(content).decode("utf-8")
            
            url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{rel_path}"
            data = {
                "message": f"Add {rel_path}",
                "content": encoded_content
            }
            
            response = requests.put(url, headers=headers, json=data, verify=False)
            
            if response.status_code in [201, 200]:
                print("OK: %s uploaded successfully" % rel_path)
                success_count += 1
            else:
                print("FAIL: %s - Status: %d, Response: %s" % (rel_path, response.status_code, response.text))
                fail_count += 1
                
        except Exception as e:
            print("ERROR: %s - %s" % (rel_path, str(e)))
            fail_count += 1
    
    print("\nResults: %d success, %d failed" % (success_count, fail_count))
    return fail_count == 0

def main():
    if len(sys.argv) < 2:
        print("ERROR: Please provide GitHub Personal Access Token")
        print("Usage: python upload_to_github.py <your_token>")
        return
    
    token = sys.argv[1]
    
    print("=" * 50)
    print("Uploading to GitHub repository: %s" % REPO_URL)
    print("=" * 50)
    
    # 上传文件
    success = upload_files(token)
    
    if success:
        print("\nSUCCESS: All files uploaded!")
    else:
        print("\nWARNING: Some files failed to upload")

if __name__ == "__main__":
    main()