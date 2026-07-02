import urllib.request
from bs4 import BeautifulSoup

urls = ["https://www.oxionics.com/", "https://en.wikipedia.org/wiki/Oxford_Ionics"]
for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, timeout=5).read()
        soup = BeautifulSoup(html, 'html.parser')
        print(f"--- {url} ---")
        print(soup.get_text(separator=' ', strip=True)[:1500])
    except Exception as e:
        print(f"Failed {url}: {e}")
