import sys, re, time
from pathlib import Path
sys.path.insert(0, str(Path.home() / 'Downloads/industrialrank'))
from build_pages import get_nav, scrape_product, generate_content, build_page, categorize, PUBLIC

url_file = 'hvacdirect_urls.txt'
limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
start = int(sys.argv[2]) if len(sys.argv) > 2 else 0

nav_html, mobile_html, search_html = get_nav()

with open(url_file) as f:
    all_urls = [l.strip() for l in f if l.strip().startswith('http')]

# Sadece gercek urun URL'leri (4+ rakamla biten) ve kategori eslesen
urls = [u for u in all_urls if re.search(r'[0-9]{4,}\.html$', u) and categorize(u)]
print(f"Gercek urun URL: {len(urls)}")

if start:
    urls = urls[start:]
    print(f"Baslangic: {start}")
if limit:
    urls = urls[:limit]
    print(f"Limit: {limit}")

stats = {'ok':0,'skip':0,'fail':0}
total = len(urls)

for i, url in enumerate(urls, 1):
    cat = categorize(url)
    slug = url.split('/')[-1].replace('.html','')
    out = PUBLIC / cat / slug / 'index.html'
    if out.exists():
        stats['skip'] += 1
        continue
    p = scrape_product(url)
    if not p:
        stats['fail'] += 1
        print(f"[{i}/{total}] SCRAPE FAIL: {url[-60:]}")
        time.sleep(1)
        continue
    c = generate_content(p)
    if not c:
        stats['fail'] += 1
        print(f"[{i}/{total}] API FAIL: {url[-60:]}")
        time.sleep(2)
        continue
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_page(p, c, cat, nav_html, mobile_html, search_html), encoding='utf-8')
    stats['ok'] += 1
    if i % 10 == 0 or i <= 5:
        print(f"[{i}/{total}] OK:{stats['ok']} SKIP:{stats['skip']} FAIL:{stats['fail']} | {p['name'][:50]}")
    time.sleep(0.4)

print(f"\nBitti: {stats}")
