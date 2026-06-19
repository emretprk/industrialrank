#!/usr/bin/env python3
"""
IndustrialRank Collection Page Generator
search-index.json'dan her kategori için tüm ürünleri listeleyen sayfa oluşturur.
"""

import json
import re
from pathlib import Path

PUBLIC_DIR = Path('/Users/emretoprak/Downloads/industrialrank/public')
INDEX_FILE = PUBLIC_DIR / 'search-index.json'

CATEGORIES = {
    'mini-splits': {
        'title': 'Mini Split Reviews 2026',
        'desc': 'Independent reviews of single-zone, multi-zone, and DIY ductless mini split systems. SEER ratings, cold-climate performance, and installed cost data.',
        'h1': 'Mini Split\nReviews 2026',
        'affiliate_url': 'https://hvacdirect.com/ductless-mini-splits.html?aff=Ob419ERXae',
        'affiliate_label': 'Shop Mini Splits',
    },
    'heat-pumps': {
        'title': 'Heat Pump Reviews 2026',
        'desc': 'Independent reviews of air source, ground source, and dual fuel heat pumps. Efficiency ratings, cold climate performance, and installation cost data.',
        'h1': 'Heat Pump\nReviews 2026',
        'affiliate_url': 'https://hvacdirect.com/heat-pump-systems.html?aff=Ob419ERXae',
        'affiliate_label': 'Shop Heat Pumps',
    },
    'air-conditioners': {
        'title': 'Air Conditioner Reviews 2026',
        'desc': 'Independent reviews of central air conditioners, window units, and portable AC systems. SEER ratings and installed cost comparisons.',
        'h1': 'Air Conditioner\nReviews 2026',
        'affiliate_url': 'https://hvacdirect.com/air-conditioner-condensers.html?aff=Ob419ERXae',
        'affiliate_label': 'Shop Air Conditioners',
    },
    'furnaces': {
        'title': 'Furnace Reviews 2026',
        'desc': 'Independent reviews of gas, electric, and two-stage furnaces. AFUE ratings, installation cost data, and brand comparisons.',
        'h1': 'Furnace\nReviews 2026',
        'affiliate_url': 'https://hvacdirect.com/furnaces.html?aff=Ob419ERXae',
        'affiliate_label': 'Shop Furnaces',
    },
    'commercial-hvac': {
        'title': 'Commercial HVAC Reviews 2026',
        'desc': 'Independent reviews of rooftop units, PTAC systems, and commercial split systems for multi-tenant and industrial buildings.',
        'h1': 'Commercial HVAC\nReviews 2026',
        'affiliate_url': 'https://hvacdirect.com/commercial-hvac-equipment.html?aff=Ob419ERXae',
        'affiliate_label': 'Shop Commercial HVAC',
    },
    'ventilation': {
        'title': 'Ventilation & Fan Reviews 2026',
        'desc': 'Independent reviews of exhaust fans, inline fans, and HVLS fans for residential, commercial, and industrial ventilation.',
        'h1': 'Ventilation\nReviews 2026',
        'affiliate_url': 'https://hvacdirect.com/ventilation-products.html?aff=Ob419ERXae',
        'affiliate_label': 'Shop Ventilation',
    },
    'air-quality': {
        'title': 'Air Quality Equipment Reviews 2026',
        'desc': 'Independent reviews of air purifiers, dehumidifiers, ERV systems, and whole-home air filters.',
        'h1': 'Air Quality\nReviews 2026',
        'affiliate_url': 'https://hvacdirect.com/air-cleaning.html?aff=Ob419ERXae',
        'affiliate_label': 'Shop Air Quality',
    },
}

NAV = open(PUBLIC_DIR / 'index.html', encoding='utf-8').read()
nav_match = re.search(r'(<nav>.*?</nav>)', NAV, re.DOTALL)
NAV_HTML = nav_match.group(1) if nav_match else ''

mobile_match = re.search(r'(<div class="mobile-menu".*?</div>\s*\n)', NAV, re.DOTALL)
MOBILE_HTML = mobile_match.group(1) if mobile_match else ''

search_match = re.search(r'(<!-- SEARCH MODAL -->.*?</script>)', NAV, re.DOTALL)
SEARCH_HTML = search_match.group(1) if search_match else ''

def star_rating(score):
    if not score:
        return ''
    try:
        s = float(score)
        full = int(s / 2)
        stars = '★' * full + '☆' * (5 - full)
        return f'{stars} {score}'
    except:
        return ''

def make_card(product):
    url = product.get('url', '')
    title = product.get('title', '')
    brand = product.get('brand', '')
    price = product.get('price', '')
    image = product.get('image', '')
    score = product.get('score', '')

    badge = brand.upper() if brand else 'REVIEW'
    img_html = f'<img src="{image}" alt="{title}" loading="lazy" referrerpolicy="no-referrer" style="width:100%;height:160px;object-fit:contain;background:#f9fafb;border-radius:6px;margin-bottom:12px">' if image else ''
    score_html = f'<div class="card-score">{star_rating(score)}</div>' if score else ''
    price_html = f'<div style="font-size:13px;font-weight:700;color:var(--ink);margin-top:4px">{price}</div>' if price else ''

    return f'''<a href="{url}" class="product-card">
      {img_html}
      <div class="card-badge">{badge}</div>
      <div class="card-title">{title}</div>
      <div class="card-desc">{brand}</div>
      {score_html}
      {price_html}
    </a>'''

def generate_page(cat, meta, products):
    h1_lines = meta['h1'].split('\n')
    h1_html = h1_lines[0] + ('<br><em>' + h1_lines[1] + '</em>' if len(h1_lines) > 1 else '')
    
    cards_html = '\n'.join(make_card(p) for p in products)
    count = len(products)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{meta['title']} | IndustrialRank</title>
<meta name="description" content="{meta['desc']}">
<link rel="canonical" href="https://industrialrank.com/{cat}/">
<link rel="icon" href="/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800;900&family=DM+Sans:wght@400;500&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<script type="application/ld+json">{{
  "@context":"https://schema.org",
  "@type":"CollectionPage",
  "name":"{meta['title']}",
  "description":"{meta['desc']}",
  "url":"https://industrialrank.com/{cat}/"
}}</script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#f5f4f0;--surface:#fff;--ink:#111;--ink2:#555;--ink3:#999;--amber:#d97706;--amber2:#fbbf24;--amber-bg:#fffbeb;--steel:#1a1f2e;--border:#e4e0d8;--border2:#ede9e2;--green:#16a34a;--red:#dc2626}}
body{{font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--ink);line-height:1.6}}
nav{{background:var(--steel);padding:0 24px;display:flex;align-items:center;justify-content:space-between;height:56px;position:sticky;top:0;z-index:100}}
.logo{{display:flex;align-items:center;gap:10px}}
.logo-text{{font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:24px;color:#fff;letter-spacing:.02em}}
.logo-text em{{color:var(--amber2);font-style:normal}}
.nav-links{{display:flex;gap:0}}
.nav-links a{{font-size:12px;font-weight:500;color:rgba(255,255,255,0.55);text-decoration:none;padding:0 14px;height:56px;display:flex;align-items:center;letter-spacing:.05em;text-transform:uppercase;border-bottom:2px solid transparent;transition:color .15s}}
.nav-links a:hover{{color:#fff;border-bottom-color:var(--amber)}}
.nav-btn{{background:var(--amber);color:var(--steel);font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:13px;letter-spacing:.08em;text-transform:uppercase;padding:8px 18px;border-radius:5px;cursor:pointer;text-decoration:none}}
.search-trigger{{background:none;border:none;color:rgba(255,255,255,0.7);cursor:pointer;padding:8px;display:flex;align-items:center;transition:color .15s;margin-right:4px}}
.search-trigger:hover{{color:#fff}}
.breadcrumb{{background:var(--surface);border-bottom:1px solid var(--border);padding:10px 40px;font-size:12px;color:var(--ink3)}}
.breadcrumb a{{color:var(--amber);text-decoration:none}}
.page-hero{{background:var(--steel);padding:48px 40px 40px}}
.page-hero h1{{font-family:'Barlow Condensed',sans-serif;font-weight:900;font-size:52px;line-height:1;text-transform:uppercase;color:#fff;margin-bottom:12px}}
.page-hero h1 em{{color:var(--amber2);font-style:normal}}
.page-hero p{{color:rgba(255,255,255,.5);font-size:16px;max-width:700px}}
.page-hero .count{{display:inline-block;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.12);border-radius:20px;padding:4px 14px;font-size:12px;color:rgba(255,255,255,.6);margin-bottom:16px;font-family:'IBM Plex Mono',monospace;letter-spacing:.06em;text-transform:uppercase}}
.section{{max-width:1200px;margin:0 auto;padding:40px 40px}}
.product-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:24px}}
.product-card{{background:var(--surface);color:inherit;border:1px solid var(--border);border-radius:10px;padding:20px;text-decoration:none;transition:border-color .15s,box-shadow .15s;display:block}}
.product-card:hover{{border-color:var(--amber);box-shadow:0 4px 16px rgba(0,0,0,.06)}}
.card-badge{{display:inline-block;background:var(--amber);color:#fff;font-family:'IBM Plex Mono',monospace;font-size:9px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding:3px 8px;border-radius:4px;margin-bottom:10px}}
.card-title{{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:20px;color:var(--ink);margin-bottom:8px}}
.card-desc{{font-size:13px;color:var(--ink2);line-height:1.5;margin-bottom:12px}}
.card-score{{font-size:12px;color:var(--amber);font-weight:600}}
.pagination{{display:flex;justify-content:center;gap:8px;padding:32px 0;margin-top:16px}}
.page-btn{{background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:8px 16px;font-size:13px;cursor:pointer;color:var(--ink);font-family:inherit;transition:all .15s}}
.page-btn:hover,.page-btn.active{{background:var(--amber);border-color:var(--amber);color:#fff}}
.affiliate-cta{{background:var(--steel);border-radius:12px;padding:36px;margin:48px 40px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:20px}}
footer{{background:#1a1f2e;color:#888;text-align:center;padding:32px 24px;margin-top:32px;font-size:.85rem}}
footer a{{color:#d97706;text-decoration:none;font-weight:600}}
@media(max-width:768px){{.product-grid{{grid-template-columns:1fr}}.page-hero{{padding:32px 16px}}.page-hero h1{{font-size:36px}}.section{{padding:32px 16px}}.breadcrumb{{padding:10px 16px}}.affiliate-cta{{margin:32px 16px}}.nav-links{{display:none}}}}
</style>
</head>
<body>

{NAV_HTML}
{MOBILE_HTML}
{SEARCH_HTML}

<div class="breadcrumb"><a href="/">Home</a> / {meta['title'].replace(' Reviews 2026','')}</div>

<div class="page-hero">
  <div class="count">{count} REVIEWS · UPDATED JUNE 2026</div>
  <h1>{h1_html}</h1>
  <p>{meta['desc']}</p>
</div>

<div class="section">
  <div class="product-grid" id="productGrid">
    {cards_html}
  </div>
</div>

<div class="affiliate-cta">
  <div>
    <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--amber);letter-spacing:.12em;text-transform:uppercase;margin-bottom:8px">Authorized Dealer</div>
    <div style="font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:28px;color:#fff;text-transform:uppercase">Browse {meta['affiliate_label'].replace('Shop ','')}<br><span style="color:var(--amber2)">HVACDirect Catalog</span></div>
    <p style="color:rgba(255,255,255,.5);font-size:14px;margin-top:8px">Single zone, multi zone, DIY, and commercial systems in stock</p>
  </div>
  <a href="{meta['affiliate_url']}" target="_blank" rel="noopener sponsored" style="display:inline-flex;align-items:center;gap:8px;background:var(--amber);color:var(--steel);font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:1.1rem;letter-spacing:.05em;text-transform:uppercase;padding:16px 32px;border-radius:6px;text-decoration:none">{meta['affiliate_label']} →</a>
</div>

<footer>
  <p style="margin-bottom:8px"><a href="/">IndustrialRank</a> — Independent industrial equipment reviews</p>
  <p>© 2026 IndustrialRank. <a href="/privacy-policy/">Privacy Policy</a></p>
</footer>

</body>
</html>'''

def main():
    with open(INDEX_FILE, encoding='utf-8') as f:
        all_products = json.load(f)

    for cat, meta in CATEGORIES.items():
        products = [p for p in all_products if p.get('category') == cat]
        if not products:
            print(f"  {cat}: urun bulunamadi, atlaniyor")
            continue

        output_path = PUBLIC_DIR / cat / 'index.html'
        output_path.parent.mkdir(parents=True, exist_ok=True)

        html = generate_page(cat, meta, products)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"  {cat}: {len(products)} urun → {output_path}")

    print(f"\nTamamlandi!")

if __name__ == '__main__':
    main()
