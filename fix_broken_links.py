#!/usr/bin/env python3
"""
IndustrialRank — Broken Link Repair Script
============================================
Root cause: three disconnected page-generation passes were run against the
site at different times, each using a different URL/slug convention, and
they were never reconciled:

  1. Homepage showcase cards + structured data — fully fictional demo
     products (Daikin VRV5, Siemens Q2200, Lennox XC21, Carrier Infinity 20,
     Filtrete 1900 MPR) that were never built as real pages.
  2. search-index.json (9,684 entries) + the 8 category listing pages
     (heat-pumps/, air-conditioners/, mini-splits/, etc.) + the sitemap.xml
     hardcoded in worker.js — built from an older product list whose slugs
     look like "/heat-pumps/100000-btu-dual-fuel-review-7685/". None of
     these folders were ever actually generated.
  3. The REAL review pages on disk — 2,723 of them, built by build_pages.py
     using the real HVACDirect product slug, e.g.
     "/heat-pumps/1-5-ton-16-seer-goodman-heat-pump-gsz160181/". Only
     heat-pumps, air-conditioners and mini-splits have any real content;
     commercial-hvac, electrical, pumps, air-quality and water-heating have
     ZERO real pages despite their listing pages showing product cards.

None of sets #1, #2 and #3 share a single URL. Every link a visitor can
click 404s; the 2,723 real, fully-written pages are orphaned (nothing on
the site links to them).

This script:
  A) Rebuilds search-index.json from the real pages on disk.
  B) Regenerates the 3 populated category pages with only real, working
     links. The 5 empty categories get a clean "coming soon" state instead
     of dead product cards.
  C) Patches the 6 broken links on the homepage to point at real category
     pages instead of nonexistent demo products.
  D) Regenerates public/sitemap.xml from real URLs only, and removes the
     hardcoded (broken) SITEMAP special-case from worker.js so it falls
     through to the static file.

Run from the repo root: python3 fix_broken_links.py
Then review the diff, commit, and push (auto-deploys via GitHub Actions).
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
PUBLIC = ROOT / 'public'
INDEX_FILE = PUBLIC / 'search-index.json'

CATEGORIES = {
    'heat-pumps': {
        'title': 'Heat Pump Reviews 2026',
        'desc': 'Independent reviews of air source, ground source, and dual fuel heat pumps. Efficiency ratings, cold climate performance, and installation cost data.',
        'h1': 'Heat Pump\nReviews 2026',
        'affiliate_url': 'https://hvacdirect.com/heat-pumps.html?aff=Ob419ERXae',
        'affiliate_label': 'Shop Heat Pumps',
    },
    'air-conditioners': {
        'title': 'Air Conditioner Reviews 2026',
        'desc': 'Independent reviews of central air conditioners, window units, and portable AC systems. SEER ratings and installed cost comparisons.',
        'h1': 'Air Conditioner\nReviews 2026',
        'affiliate_url': 'https://hvacdirect.com/air-conditioners.html?aff=Ob419ERXae',
        'affiliate_label': 'Shop Air Conditioners',
    },
    'mini-splits': {
        'title': 'Mini Split Reviews 2026',
        'desc': 'Independent reviews of single-zone, multi-zone, and DIY ductless mini split systems. SEER ratings, cold-climate performance, and installed cost data.',
        'h1': 'Mini Split\nReviews 2026',
        'affiliate_url': 'https://hvacdirect.com/ductless-mini-splits.html?aff=Ob419ERXae',
        'affiliate_label': 'Shop Mini Splits',
    },
    'electrical': {
        'title': 'Electrical Equipment Reviews 2026',
        'desc': 'Independent reviews of load centers, circuit breakers, surge protectors, multimeters, and wiring tools.',
        'h1': 'Electrical\nReviews 2026',
        'affiliate_url': 'https://hvacdirect.com/electrical-and-solar.html?aff=Ob419ERXae',
        'affiliate_label': 'Shop Electrical',
    },
    'pumps': {
        'title': 'Industrial Pump Reviews 2026',
        'desc': 'Independent reviews of centrifugal pumps, sump pumps, circulator pumps, and fluid handling equipment.',
        'h1': 'Pump\nReviews 2026',
        'affiliate_url': 'https://hvacdirect.com/water-pools-plumbing.html?aff=Ob419ERXae',
        'affiliate_label': 'Shop Pumps',
    },
    'commercial-hvac': {
        'title': 'Commercial HVAC Reviews 2026',
        'desc': 'Independent reviews of rooftop units, VRF systems, chillers, and commercial heat pumps.',
        'h1': 'Commercial HVAC\nReviews 2026',
        'affiliate_url': 'https://hvacdirect.com/?aff=Ob419ERXae',
        'affiliate_label': 'Shop Commercial HVAC',
    },
    'water-heating': {
        'title': 'Water Heater Reviews 2026',
        'desc': 'Independent reviews of heat pump water heaters, tankless systems, and solar water heating.',
        'h1': 'Water Heater\nReviews 2026',
        'affiliate_url': 'https://hvacdirect.com/water-heating.html?aff=Ob419ERXae',
        'affiliate_label': 'Shop Water Heaters',
    },
    'air-quality': {
        'title': 'Air Quality Equipment Reviews 2026',
        'desc': 'Independent reviews of air purifiers, dehumidifiers, ERV systems, and whole-home air filters.',
        'h1': 'Air Quality\nReviews 2026',
        'affiliate_url': 'https://hvacdirect.com/air-cleaning.html?aff=Ob419ERXae',
        'affiliate_label': 'Shop Air Quality',
    },
}

STATIC_PAGES = ['', 'heat-pumps/', 'air-conditioners/', 'mini-splits/', 'commercial-hvac/',
                 'electrical/', 'pumps/', 'air-quality/', 'water-heating/', 'compare/',
                 'top10/', 'blog/', 'find/', 'about/', 'contact/', 'privacy-policy/']


# ---------------------------------------------------------------------------
# A) Rebuild search-index.json from the real pages on disk
# ---------------------------------------------------------------------------
def extract_product(idx_file):
    html = idx_file.read_text(encoding='utf-8', errors='ignore')
    m = re.search(r'"@type":\s*"Product".*?"name":\s*"((?:[^"\\]|\\.)*)".*?"price":\s*"([^"]*)"', html, re.DOTALL)
    if not m:
        return None
    name = m.group(1).replace('\\"', '"')
    price_raw = m.group(2)
    price = f'${price_raw}' if price_raw and not price_raw.startswith('$') else price_raw
    img_m = re.search(r'<img src="(https://hvacdirect\.com/[^"]+)"', html)
    image = img_m.group(1) if img_m else ''
    score_m = re.search(r'score-num-big">([0-9.]+)', html)
    score = score_m.group(1) if score_m else ''
    return {'title': name, 'price': price, 'image': image, 'score': score, 'brand': name.split()[0]}


def rebuild_search_index():
    products = []
    for cat in CATEGORIES:
        cat_dir = PUBLIC / cat
        if not cat_dir.exists():
            continue
        for sub in sorted(cat_dir.iterdir()):
            if not sub.is_dir():
                continue
            idx = sub / 'index.html'
            if not idx.exists():
                continue
            data = extract_product(idx)
            if not data:
                continue
            data['url'] = f'/{cat}/{sub.name}/'
            data['category'] = cat
            products.append(data)

    INDEX_FILE.write_text(json.dumps(products, ensure_ascii=False), encoding='utf-8')
    print(f"[A] search-index.json rebuilt: {len(products)} real products (was 9,684 fake entries)")
    by_cat = {}
    for p in products:
        by_cat.setdefault(p['category'], 0)
        by_cat[p['category']] += 1
    for c in CATEGORIES:
        print(f"      {c}: {by_cat.get(c, 0)}")
    return products


# ---------------------------------------------------------------------------
# B) Regenerate category pages (real grid, or "coming soon" if empty)
# ---------------------------------------------------------------------------
def star_rating(score):
    if not score:
        return ''
    try:
        s = float(score)
        full = int(s / 2)
        return f"{'★' * full}{'☆' * (5 - full)} {score}"
    except Exception:
        return ''


def make_card(p):
    badge = p['brand'].upper() if p['brand'] else 'REVIEW'
    img_html = (f'<img src="{p["image"]}" alt="{p["title"]}" loading="lazy" referrerpolicy="no-referrer" '
                f'style="width:100%;height:160px;object-fit:contain;background:#f9fafb;border-radius:6px;margin-bottom:12px">'
                if p['image'] else '')
    score_html = f'<div class="card-score">{star_rating(p["score"])}</div>' if p['score'] else ''
    price_html = f'<div style="font-size:13px;font-weight:700;color:var(--ink);margin-top:4px">{p["price"]}</div>' if p['price'] else ''
    return f'''<a href="{p['url']}" class="product-card">
      {img_html}
      <div class="card-badge">{badge}</div>
      <div class="card-title">{p['title']}</div>
      <div class="card-desc">{p['brand']}</div>
      {score_html}
      {price_html}
    </a>'''


PAGE_HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | IndustrialRank</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://industrialrank.com/{cat}/">
<link rel="icon" href="/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800;900&family=DM+Sans:wght@400;500&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<script type="application/ld+json">{{
  "@context":"https://schema.org",
  "@type":"CollectionPage",
  "name":"{title}",
  "description":"{desc}",
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
.empty-state{{text-align:center;padding:64px 24px;color:var(--ink2)}}
.empty-state h2{{font-family:'Barlow Condensed',sans-serif;font-size:28px;color:var(--ink);margin-bottom:12px;text-transform:uppercase}}
.affiliate-cta{{background:var(--steel);border-radius:12px;padding:36px;margin:48px 40px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:20px}}
footer{{background:#1a1f2e;color:#888;text-align:center;padding:32px 24px;margin-top:32px;font-size:.85rem}}
footer a{{color:#d97706;text-decoration:none;font-weight:600}}
@media(max-width:768px){{.product-grid{{grid-template-columns:1fr}}.page-hero{{padding:32px 16px}}.page-hero h1{{font-size:36px}}.section{{padding:32px 16px}}.breadcrumb{{padding:10px 16px}}.affiliate-cta{{margin:32px 16px}}.nav-links{{display:none}}}}
</style>
</head>
<body>

{nav_html}
{mobile_html}
{search_html}

<div class="breadcrumb"><a href="/">Home</a> / {title_short}</div>

<div class="page-hero">
  <div class="count">{count_label}</div>
  <h1>{h1_html}</h1>
  <p>{desc}</p>
</div>

<div class="section">
{body}
</div>

<div class="affiliate-cta">
  <div>
    <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--amber);letter-spacing:.12em;text-transform:uppercase;margin-bottom:8px">Authorized Dealer</div>
    <div style="font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:28px;color:#fff;text-transform:uppercase">Browse {affiliate_label_short}<br><span style="color:var(--amber2)">HVACDirect Catalog</span></div>
    <p style="color:rgba(255,255,255,.5);font-size:14px;margin-top:8px">Single zone, multi zone, DIY, and commercial systems in stock</p>
  </div>
  <a href="{affiliate_url}" target="_blank" rel="noopener sponsored" style="display:inline-flex;align-items:center;gap:8px;background:var(--amber);color:var(--steel);font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:1.1rem;letter-spacing:.05em;text-transform:uppercase;padding:16px 32px;border-radius:6px;text-decoration:none">{affiliate_label} →</a>
</div>

<footer>
  <p style="margin-bottom:8px"><a href="/">IndustrialRank</a> — Independent industrial equipment reviews</p>
  <p>© 2026 IndustrialRank. <a href="/privacy-policy/">Privacy Policy</a></p>
</footer>

</body>
</html>'''


def regenerate_category_pages(products):
    nav_src = (PUBLIC / 'index.html').read_text(encoding='utf-8')
    nav_html = (re.search(r'(<nav>.*?</nav>)', nav_src, re.DOTALL) or [None, ''])[1]
    mobile_html = (re.search(r'(<div class="mobile-menu".*?</div>\s*\n)', nav_src, re.DOTALL) or [None, ''])[1]
    search_html = (re.search(r'(<!-- SEARCH MODAL -->.*?</script>)', nav_src, re.DOTALL) or [None, ''])[1]

    by_cat = {}
    for p in products:
        by_cat.setdefault(p['category'], []).append(p)

    for cat, meta in CATEGORIES.items():
        items = by_cat.get(cat, [])
        h1_lines = meta['h1'].split('\n')
        h1_html = h1_lines[0] + (f"<br><em>{h1_lines[1]}</em>" if len(h1_lines) > 1 else '')

        if items:
            body = f'<div class="product-grid" id="productGrid">\n' + '\n'.join(make_card(p) for p in items) + '\n</div>'
            count_label = f"{len(items)} REVIEWS · UPDATED JUNE 2026"
        else:
            body = (f'<div class="empty-state"><h2>Reviews coming soon</h2>'
                    f'<p>We are independently testing {meta["affiliate_label"].replace("Shop ", "").lower()} '
                    f'and publishing reviews here shortly. In the meantime, browse the live catalog below.</p></div>')
            count_label = "0 REVIEWS PUBLISHED YET"

        html = PAGE_HEAD.format(
            title=meta['title'], desc=meta['desc'], cat=cat,
            nav_html=nav_html, mobile_html=mobile_html, search_html=search_html,
            title_short=meta['title'].replace(' Reviews 2026', ''),
            count_label=count_label, h1_html=h1_html, body=body,
            affiliate_label_short=meta['affiliate_label'].replace('Shop ', ''),
            affiliate_url=meta['affiliate_url'], affiliate_label=meta['affiliate_label'],
        )
        out = PUBLIC / cat / 'index.html'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding='utf-8')
        print(f"[B] {cat}/index.html regenerated — {len(items)} real product(s)" if items
              else f"[B] {cat}/index.html regenerated — coming-soon state (0 real products)")


# ---------------------------------------------------------------------------
# C) Patch the 6 broken homepage links
# ---------------------------------------------------------------------------
HOMEPAGE_LINK_FIXES = {
    'https://industrialrank.com/electrical/siemens-q2200-review/': 'https://industrialrank.com/electrical/',
    '/electrical/siemens-q2200-review/': '/electrical/',
    'https://industrialrank.com/hvac/daikin-vrv5-review/': 'https://industrialrank.com/mini-splits/',
    '/hvac/daikin-vrv5-review/': '/mini-splits/',
    'https://industrialrank.com/hvac/carrier-infinity-20-heat-pump-review/': 'https://industrialrank.com/heat-pumps/',
    '/hvac/carrier-infinity-20-heat-pump-review/': '/heat-pumps/',
    'https://industrialrank.com/hvac/filtrete-1900-mpr-review': 'https://industrialrank.com/air-quality/',
    '/hvac/filtrete-1900-mpr-review': '/air-quality/',
    'https://industrialrank.com/hvac/lennox-xc21-review': 'https://industrialrank.com/air-conditioners/',
    '/hvac/lennox-xc21-review': '/air-conditioners/',
    'href="/guides/"': 'href="/blog/"',
}


def fix_homepage():
    f = PUBLIC / 'index.html'
    html = f.read_text(encoding='utf-8')
    changed = 0
    for old, new in HOMEPAGE_LINK_FIXES.items():
        count = html.count(old)
        if count:
            html = html.replace(old, new)
            changed += count
    f.write_text(html, encoding='utf-8')
    print(f"[C] index.html: {changed} broken reference(s) repointed to real, working category pages")


# ---------------------------------------------------------------------------
# D) Regenerate sitemap.xml as a static file; strip the dead one from worker.js
# ---------------------------------------------------------------------------
def regenerate_sitemap(products):
    urls = []
    for p in STATIC_PAGES:
        urls.append(f"https://industrialrank.com/{p}")
    for prod in products:
        urls.append(f"https://industrialrank.com{prod['url']}")

    entries = '\n'.join(
        f'  <url><loc>{u}</loc><lastmod>2026-06-18</lastmod>'
        f'<changefreq>{"weekly" if u.count("/") <= 4 else "monthly"}</changefreq>'
        f'<priority>{"1.0" if u == "https://industrialrank.com/" else "0.8"}</priority></url>'
        for u in urls
    )
    sitemap = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}\n</urlset>\n'
    (PUBLIC / 'sitemap.xml').write_text(sitemap, encoding='utf-8')
    print(f"[D] public/sitemap.xml regenerated — {len(urls)} real URLs (was ~70 hardcoded, mostly broken)")

    worker = ROOT / 'worker.js'
    src = worker.read_text(encoding='utf-8')
    src2 = re.sub(r'const SITEMAP = `.*?`;\n\n', '', src, flags=re.DOTALL)
    src2 = re.sub(
        r"\s*// Sitemap\n\s*if \(url\.pathname === '/sitemap\.xml'\) \{\n.*?\n\s*\}\n",
        '\n',
        src2, flags=re.DOTALL,
    )
    if src2 != src:
        worker.write_text(src2, encoding='utf-8')
        print("[D] worker.js: removed hardcoded broken SITEMAP, now serves the static sitemap.xml from /public")
    else:
        print("[D] worker.js: WARNING — could not auto-strip old SITEMAP block, please check manually")


def verify(products):
    """Sanity check: confirm 0% broken links remain across every category page."""
    broken = 0
    checked = 0
    for cat in CATEGORIES:
        f = PUBLIC / cat / 'index.html'
        if not f.exists():
            continue
        for href in re.findall(rf'href="(/{cat}/[a-z0-9-]+/)"', f.read_text(encoding='utf-8')):
            checked += 1
            if not (PUBLIC / href.strip('/') / 'index.html').exists():
                broken += 1
    print(f"\n[VERIFY] {checked} product links checked across category pages — {broken} broken")


if __name__ == '__main__':
    products = rebuild_search_index()
    regenerate_category_pages(products)
    fix_homepage()
    regenerate_sitemap(products)
    verify(products)
    print("\nDone. Review the diff (git status / git diff), then:")
    print("  git add -A && git commit -m 'Fix: repoint all links to real generated review pages' && git push")
