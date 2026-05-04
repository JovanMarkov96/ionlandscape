import urllib.request
from bs4 import BeautifulSoup
import json
import re

urls = [
    "https://en.wikipedia.org/wiki/QuEra",
    "https://en.wikipedia.org/wiki/QuEra_Computing",
    "https://www.quera.com/about",
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, timeout=5).read()
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        # simplistic grep for CEO
        match = re.search(r'.{0,50}CEO.{0,50}', text)
        print(f"URL: {url}")
        print(f"Found CEO context: {match.group(0) if match else 'None'}")
        
    except Exception as e:
        pass
