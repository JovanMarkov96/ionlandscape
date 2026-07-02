import urllib.request
from bs4 import BeautifulSoup
import re

url = "https://www.quera.com/about"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req, timeout=5).read()
soup = BeautifulSoup(html, 'html.parser')
text = soup.get_text(separator=' ', strip=True)

for match in re.finditer(r'.{0,60}CEO.{0,60}', text, re.IGNORECASE):
    print(match.group(0))
