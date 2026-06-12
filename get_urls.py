import requests, re
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}

r = requests.get('https://hvacdirect.com/sitemap.xml', headers=headers)
sitemaps = re.findall(r'<loc>(https://hvacdirect\.com/media/[^<]+)</loc>', r.text)

all_urls = []
for sm in sitemaps:
    print(f"Cekiliyor: {sm}")
    r2 = requests.get(sm, headers=headers, timeout=15)
    urls = re.findall(r'<loc>(https://hvacdirect\.com/[^<]+\.html)</loc>', r2.text)
    # Sadece ürün sayfaları (kategori değil)
    product_urls = [u for u in urls if u.count('/') == 3]
    all_urls.extend(product_urls)
    print(f"  {len(product_urls)} urun URL'si")

# Kaydet
with open('hvacdirect_urls.txt', 'w') as f:
    for u in all_urls:
        f.write(u + '\n')

print(f"\nToplam: {len(all_urls)} urun URL'si")
print("Kaydedildi: hvacdirect_urls.txt")
