import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', 'Referer': 'https://www.google.com/'}

url = 'https://hvacdirect.com/mrcool-diy-5th-gen-e-star-12000-btu-single-zone-mini-split-complete-system-with-25ft-line-set-115v-diy-12-hp-wm-115d25-o.html'

r = requests.get(url, headers=HEADERS, timeout=15)
soup = BeautifulSoup(r.text, 'html.parser')

# Ürün adı
name = soup.find('h1')
print("Ad:", name.text.strip() if name else "YOK")

# Fiyat
price = soup.find('meta', property='product:price:amount')
print("Fiyat:", '$'+price['content'] if price else "YOK")

# Görsel
img = soup.find('meta', property='og:image')
print("Gorsel:", img['content'][:80] if img else "YOK")

# SKU / Model
sku = soup.find('meta', property='product:retailer_item_id') or soup.find('div', class_='product-info-sku')
print("SKU:", sku.text.strip() if sku else "YOK")

# Specs tablosu
specs = soup.find_all('tr')
print(f"\nSpec satirlari: {len(specs)}")
for row in specs[:10]:
    cols = row.find_all(['td','th'])
    if len(cols) >= 2:
        print(f"  {cols[0].text.strip()}: {cols[1].text.strip()}")
