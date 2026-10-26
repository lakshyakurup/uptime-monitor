import urllib.request

def check_url(url):
    try:
        response = urllib.request.urlopen(url, timeout=5)
        print(f"[{response.status}] {url} is UP")
    except Exception as e:
        print(f"[DOWN] {url} - Error: {e}")

if __name__ == "__main__":
    check_url("https://github.com")
