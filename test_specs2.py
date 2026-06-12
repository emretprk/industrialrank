import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', 'Referer': 'https://www.google.com/'}

url = 'https://hvacdirect.com/mrcool-diy-5th-gen-e-star-12000-btu-single-zone-mini-split-complete-system-with-25ft-line-set-115v-diy-12-hp-wm-115d25-o.html'

r = requests.get(url, headers=HEADERS, timeout=15)
soup = BeautifulSoup(r.text, 'html.parser')

specs = {}
for row in soup.find_all('tr'):
    cols = row.find_all(['td','th'])
    if len(cols) >= 2:
        key = cols[0].text.strip()
        val = cols[1].text.strip()
        if key: specs[key] = val

for k, v in specs.items():
    print(f"{k}: {v}")
