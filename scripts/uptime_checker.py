import urllib.request
import time
import sys

targets_file = "targets.txt"

def check_site(url):
    url = url.strip()
    if not url:
        return
    try:
        start_time = time.time()
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            latency = round((time.time() - start_time) * 1000, 2)
            print(f"[ONLINE] {url} - Status: {response.status} - Response Time: {latency}ms")
    except Exception as e:
        print(f"[OFFLINE] {url} - Error: {e}")

def main():
    print("--- Running Uptime Monitor Checks ---")
    try:
        with open(targets_file, "r") as f:
            urls = f.readlines()
            for url in urls:
                check_site(url)
    except FileNotFoundError:
        print(f"Error: {targets_file} not found.")

if __name__ == "__main__":
    main()
