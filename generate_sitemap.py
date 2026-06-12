from pathlib import Path
from datetime import date

public = Path('public')
today = date.today().isoformat()
urls = []

for html in public.rglob('index.html'):
    parts = html.parts
    # Ana index.html'leri atla
    if len(parts) <= 2:
        continue
    # Kategori index.html'lerini atla
    if len(parts) == 3:
        continue
    # Ürün sayfaları
    slug_path = '/'.join(parts[1:-1])
    urls.append(f'https://industrialrank.com/{slug_path}/')

print(f"Toplam URL: {len(urls)}")

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url in urls:
    sitemap += f'  <url>\n    <loc>{url}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n'
sitemap += '</urlset>'

Path('public/sitemap.xml').write_text(sitemap, encoding='utf-8')
print("public/sitemap.xml olusturuldu.")
