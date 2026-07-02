import urllib.request
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/QuEra_Computing"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req, timeout=5).read()
soup = BeautifulSoup(html, 'html.parser')
print(soup.get_text(separator=' ', strip=True)[:1500])
