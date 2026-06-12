import requests, re
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
url = 'https://hvacdirect.com/mrcool-diy-5th-gen-e-star-12000-btu-single-zone-mini-split-complete-system-with-25ft-line-set-115v-diy-12-hp-wm-115d25-o.html'

r = requests.get(url, headers=headers, timeout=15)
soup = BeautifulSoup(r.text, 'html.parser')

# Ürün adı
name = soup.find('h1')
print("Ad:", name.text.strip() if name else "YOK")

# Fiyat
price = soup.find('meta', property='product:price:amount')
print("Fiyat:", price['content'] if price else "YOK")

# OG görsel
img = soup.find('meta', property='og:image')
print("Gorsel:", img['content'][:80] if img else "YOK")

# Marka
brand = soup.find('meta', property='product:brand')
print("Marka:", brand['content'] if brand else "YOK")
