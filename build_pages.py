#!/usr/bin/env python3
"""
IndustrialRank - Full Page Builder
HVACDirect'ten scrape + Claude API ile içerik + mevcut template
"""

import requests, json, time, re, os
from bs4 import BeautifulSoup
from pathlib import Path

ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Referer': 'https://www.google.com/'
}
AFF_CODE = '?affiliate_code=Ob419ERXae&referring_service=link'
PUBLIC = Path('public')

# Mevcut index.html'den nav HTML'ini çek
def get_nav():
    nav_html = '''<nav style="background:#1a1f2e;padding:0 32px;display:flex;align-items:center;justify-content:space-between;height:56px;position:sticky;top:0;z-index:100">
  <a href="/" style="font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:22px;color:#fff;text-decoration:none">Industrial<em style="color:#fbbf24;font-style:normal">Rank</em></a>
  <div style="display:flex;gap:4px;align-items:center">
    <a href="/mini-splits/" style="font-size:12px;color:rgba(255,255,255,.55);text-decoration:none;padding:6px 12px;text-transform:uppercase;letter-spacing:.04em">Mini Splits</a>
    <a href="/heat-pumps/" style="font-size:12px;color:rgba(255,255,255,.55);text-decoration:none;padding:6px 12px;text-transform:uppercase;letter-spacing:.04em">Heat Pumps</a>
    <a href="/air-conditioners/" style="font-size:12px;color:rgba(255,255,255,.55);text-decoration:none;padding:6px 12px;text-transform:uppercase;letter-spacing:.04em">AC</a>
    <a href="/furnaces/" style="font-size:12px;color:rgba(255,255,255,.55);text-decoration:none;padding:6px 12px;text-transform:uppercase;letter-spacing:.04em">Furnaces</a>
    <a href="/commercial-hvac/" style="font-size:12px;color:rgba(255,255,255,.55);text-decoration:none;padding:6px 12px;text-transform:uppercase;letter-spacing:.04em">Commercial</a>
    <a href="/ventilation/" style="font-size:12px;color:rgba(255,255,255,.55);text-decoration:none;padding:6px 12px;text-transform:uppercase;letter-spacing:.04em">Ventilation</a>
    <a href="/air-quality/" style="font-size:12px;color:rgba(255,255,255,.55);text-decoration:none;padding:6px 12px;text-transform:uppercase;letter-spacing:.04em">Air Quality</a>
    <a href="/find/" style="background:#d97706;color:#1a1f2e;font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:13px;text-transform:uppercase;padding:8px 16px;border-radius:5px;text-decoration:none">Find Equipment</a>
  </div>
</nav>'''
    return nav_html, '', ''

def categorize(url):
    u = url.lower()
    excl = ['bbq', 'grill', 'fireplace', 'fire-pit', 'firepit', 'patio-heater',
            'outdoor-furniture', 'stove', 'chimney', 'smart-toilet', 'toilet',
            'generator', 'solar-panel', 'solar-powered', 'laser-cutting',
            'ice-maker', 'water-cooler', 'drinking-fountain', 'gas-log',
            'outdoor-kitchen', 'beverage-air']
    if any(p in u for p in excl): return None
    if 'mini-split' in u or 'ductless' in u: return 'mini-splits'
    if 'heat-pump' in u: return 'heat-pumps'
    if 'air-condition' in u or 'central-air' in u or 'condenser' in u: return 'air-conditioners'
    if 'furnace' in u: return 'furnaces'
    if 'commercial' in u or 'ptac' in u or 'multi-tenant' in u or 'air-handler' in u or 'make-up-air' in u or 'air-curtain' in u: return 'commercial-hvac'
    if 'fan' in u or 'ventilation' in u or 'exhaust' in u or 'hvls' in u or 'evaporative-cooler' in u: return 'ventilation'
    if 'dehumidifier' in u or 'air-purifier' in u or 'hepa' in u or 'erv' in u or 'hrv' in u or 'air-filter' in u or 'iaq' in u or 'uv-light' in u or 'odor-control' in u: return 'air-quality'
    return None

def scrape_product(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code != 200: return None
        soup = BeautifulSoup(r.text, 'html.parser')
        
        name = soup.find('h1')
        price = soup.find('meta', property='product:price:amount')
        image = soup.find('meta', property='og:image')
        desc = soup.find('meta', {'name': 'description'})
        
        specs = {}
        for row in soup.find_all('tr'):
            cols = row.find_all(['td', 'th'])
            if len(cols) >= 2:
                key = cols[0].text.strip()
                val = cols[1].text.strip()
                if key and len(key) < 60 and val and 'Proposition 65' not in key:
                    specs[key] = val
        
        if not name or not name.text.strip():
            return None
            
        return {
            'name': name.text.strip(),
            'price': '$' + price['content'] if price else '',
            'price_raw': price['content'] if price else '0',
            'image': image['content'] if image else '',
            'description': desc['content'] if desc else '',
            'url': url,
            'aff_url': url + AFF_CODE,
            'specs': specs
        }
    except Exception as e:
        return None

def generate_content(product):
    prompt = f"""You are a technical writer for IndustrialRank, an independent HVAC equipment review site trusted by contractors and homeowners.

Product: {product['name']}
Price: {product['price']}
Specs:
{json.dumps(product['specs'], indent=2)}

Write a comprehensive, honest product review. Be specific and data-driven. Use the actual spec numbers.

CRITICAL RULES:
- Never use em dashes (use commas or restructure sentences instead)
- Write like a knowledgeable human, not a robot
- Be specific about numbers: BTU, SEER2, voltage, etc.
- Mention real use cases

Return ONLY valid JSON (no markdown, no backticks):
{{
  "tagline": "One sharp sentence capturing key value (under 15 words)",
  "ir_score": {{
    "overall": 8.2,
    "efficiency": 8.5,
    "reliability": 7.8,
    "value": 8.0,
    "installation": 8.5,
    "warranty": 8.0
  }},
  "bottom_line": "2-3 sentences on who this is best for and why. Be specific.",
  "pros": ["specific pro with data", "specific pro with data", "specific pro with data", "specific pro", "specific pro"],
  "cons": ["specific con", "specific con", "specific con"],
  "who_should_buy": "2 sentences about ideal buyer. Be specific about use case.",
  "who_should_avoid": "1 sentence about who should look elsewhere.",
  "review_p1": "First paragraph introducing the product and its market position (80-100 words). No em dashes.",
  "review_p2": "Second paragraph covering performance and efficiency details using actual spec numbers (80-100 words). No em dashes.",
  "install_section": "Installation requirements and complexity (60-80 words). No em dashes.",
  "warranty_section": "Warranty coverage and what it means for buyers (50-70 words). No em dashes.",
  "faq": [
    {{"q": "Specific question about this product", "a": "Detailed answer using spec data (40-60 words)"}},
    {{"q": "Installation or compatibility question", "a": "Practical answer (40-60 words)"}},
    {{"q": "Efficiency or performance question", "a": "Data-backed answer (40-60 words)"}},
    {{"q": "Comparison or alternatives question", "a": "Honest comparison (40-60 words)"}},
    {{"q": "Warranty or support question", "a": "Clear answer (30-50 words)"}}
  ]
}}"""

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": 2000,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30
        )
        data = response.json()
        text = data['content'][0]['text'].strip()
        # Clean JSON
        if '```' in text:
            text = re.search(r'\{.*\}', text, re.DOTALL).group(0)
        return json.loads(text)
    except Exception as e:
        return None

def score_bar(score):
    pct = int((score / 10) * 100)
    return f'<div class="score-bar"><div class="score-fill" style="width:{pct}%"></div></div>'

def build_page(product, content, category, nav_html, mobile_html, search_html):
    name = product['name']
    price = product['price']
    image = product['image']
    aff_url = product['aff_url']
    specs = product['specs']
    
    # IR Score
    ir = content.get('ir_score', {})
    overall = ir.get('overall', 8.0)
    
    # Specs table rows
    key_specs = ['SKU', 'Brand/Manufacturer', 'Cooling BTU', 'Heating BTU', 'Refrigerant', 
                 'Electrical', 'BTU/Tonnage', 'Mini Split Type', 'Zone Compatibility',
                 'Warranty', 'Decibel Level (dBA)', 'Weight (in lbs)']
    spec_rows = ''
    for k in key_specs:
        if k in specs:
            spec_rows += f'<tr><td>{k}</td><td class="spec-highlight">{specs[k]}</td></tr>'
    
    # Additional specs
    shown = set(key_specs)
    for k, v in specs.items():
        if k not in shown and len(spec_rows) < 3000:
            spec_rows += f'<tr><td>{k}</td><td>{v}</td></tr>'

    # Pros/Cons
    pros_html = ''.join(f'<li>{p}</li>' for p in content.get('pros', []))
    cons_html = ''.join(f'<li>{c}</li>' for c in content.get('cons', []))
    
    # FAQ
    faq_schema = []
    faq_html = ''
    for item in content.get('faq', []):
        q = item.get('q', '')
        a = item.get('a', '')
        faq_html += f'''<div class="faq-item">
          <div class="faq-q" onclick="this.nextElementSibling.classList.toggle('open')">{q} <span>+</span></div>
          <div class="faq-a">{a}</div>
        </div>'''
        faq_schema.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    
    # Schema
    schema = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Product",
                "name": name,
                "description": content.get('bottom_line', ''),
                "offers": {
                    "@type": "Offer",
                    "url": aff_url,
                    "priceCurrency": "USD",
                    "price": product.get('price_raw', ''),
                    "availability": "https://schema.org/InStock"
                }
            },
            {
                "@type": "FAQPage",
                "mainEntity": faq_schema
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://industrialrank.com/"},
                    {"@type": "ListItem", "position": 2, "name": category.replace('-', ' ').title(), "item": f"https://industrialrank.com/{category}/"},
                    {"@type": "ListItem", "position": 3, "name": name}
                ]
            }
        ]
    })

    slug = product['url'].split('/')[-1].replace('.html', '')
    canonical = f"https://industrialrank.com/{category}/{slug}/"

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} Review 2026 | IndustrialRank</title>
<meta name="description" content="{content.get('bottom_line', '')[:155]}">
<link rel="canonical" href="{canonical}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800;900&family=DM+Sans:wght@400;500&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<script type="application/ld+json">{schema}</script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#f5f4f0;--surface:#fff;--ink:#111;--ink2:#555;--ink3:#999;--amber:#d97706;--amber2:#fbbf24;--amber-bg:#fffbeb;--steel:#1a1f2e;--border:#e4e0d8;--border2:#ede9e2;--green:#16a34a;--red:#dc2626}}
body{{background:var(--bg);color:var(--ink);font-family:'DM Sans',sans-serif;line-height:1.6}}
nav{{background:var(--steel);padding:0 40px;display:flex;align-items:center;justify-content:space-between;height:56px;position:sticky;top:0;z-index:100}}
.logo{{display:flex;align-items:center;gap:10px;text-decoration:none}}
.logo img{{height:32px;width:auto}}
.logo-text{{font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:22px;color:#fff;text-decoration:none}}
.logo-text em{{color:var(--amber2);font-style:normal}}
.nav-links{{display:flex;gap:0}}
.nav-links a{{font-size:12px;font-weight:500;color:rgba(255,255,255,0.55);text-decoration:none;padding:0 14px;height:56px;display:flex;align-items:center;letter-spacing:0.05em;text-transform:uppercase;border-bottom:2px solid transparent;transition:color 0.15s}}
.nav-links a:hover{{color:#fff;border-bottom-color:var(--amber)}}
.nav-btn{{background:var(--amber);color:var(--steel);font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:13px;letter-spacing:0.08em;text-transform:uppercase;padding:8px 18px;border:none;border-radius:5px;cursor:pointer;text-decoration:none}}
.search-trigger{{background:none;border:none;color:rgba(255,255,255,0.7);cursor:pointer;padding:8px;display:flex;align-items:center;margin-right:4px}}
.breadcrumb{{background:var(--surface);border-bottom:1px solid var(--border);padding:10px 40px;font-size:12px;color:var(--ink3)}}
.breadcrumb a{{color:var(--amber);text-decoration:none}}
.review-hero{{background:var(--steel);padding:48px 40px 0}}
.review-hero-inner{{max-width:1100px;margin:0 auto}}
.review-tag{{display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.12);border-radius:20px;padding:4px 14px;margin-bottom:16px;font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--amber2);letter-spacing:0.1em;text-transform:uppercase}}
h1{{font-family:'Barlow Condensed',sans-serif;font-weight:900;font-size:48px;line-height:1;text-transform:uppercase;color:#fff;margin-bottom:16px}}
.hero-layout{{display:grid;grid-template-columns:1fr 340px;gap:40px;align-items:start;padding-bottom:40px}}
.hero-left h1{{font-size:42px}}
.tagline{{font-size:16px;color:rgba(255,255,255,0.6);margin-bottom:24px;line-height:1.5}}
.hero-img{{background:rgba(255,255,255,0.04);border-radius:12px;overflow:hidden;display:flex;align-items:center;justify-content:center;min-height:280px;padding:16px}}
.hero-img img{{max-width:100%;max-height:280px;object-fit:contain}}
.product-hero-img{{display:none}}
.buy-box{{background:var(--surface);border-radius:12px;padding:24px;margin-top:24px}}
.price-range{{font-family:'Barlow Condensed',sans-serif;font-weight:900;font-size:36px;color:var(--amber);margin:4px 0 12px}}
.buy-btn{{display:block;width:100%;background:var(--amber);color:var(--steel);font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:16px;letter-spacing:0.08em;text-transform:uppercase;padding:14px;border-radius:8px;text-align:center;text-decoration:none;margin-bottom:10px}}
.buy-btn:hover{{opacity:0.9}}
.buy-btn-sec{{display:block;width:100%;background:transparent;color:var(--amber);font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:14px;letter-spacing:0.08em;text-transform:uppercase;padding:12px;border:2px solid var(--amber);border-radius:8px;text-align:center;text-decoration:none}}
.score-box{{background:var(--steel);border-radius:12px;padding:20px;margin-top:16px}}
.score-overall{{text-align:center;padding-bottom:16px;margin-bottom:16px;border-bottom:1px solid rgba(255,255,255,0.1)}}
.score-num-big{{font-family:'Barlow Condensed',sans-serif;font-weight:900;font-size:56px;color:var(--amber2);line-height:1}}
.score-label-big{{font-family:'IBM Plex Mono',monospace;font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:0.1em;text-transform:uppercase}}
.score-row{{display:flex;justify-content:space-between;align-items:center;padding:6px 0}}
.score-label-s{{font-size:12px;color:rgba(255,255,255,0.6)}}
.score-bar-wrap{{display:flex;align-items:center;gap:8px}}
.score-bar{{height:4px;background:rgba(255,255,255,0.15);border-radius:2px;width:80px;overflow:hidden}}
.score-fill{{height:100%;background:var(--amber);border-radius:2px}}
.score-num{{font-family:'IBM Plex Mono',monospace;font-size:11px;color:rgba(255,255,255,0.7)}}
.review-body{{max-width:1100px;margin:0 auto;padding:48px 40px;display:grid;grid-template-columns:1fr 320px;gap:48px;align-items:start}}
.content h2{{font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:26px;text-transform:uppercase;color:var(--ink);margin:36px 0 14px;padding-top:4px;border-top:3px solid var(--amber)}}
.content p{{font-size:15px;color:var(--ink2);margin-bottom:16px;line-height:1.7}}
.content ul{{margin:0 0 16px 20px}}
.content ul li{{font-size:15px;color:var(--ink2);margin-bottom:8px;line-height:1.6}}
.bottom-line-box{{background:var(--amber-bg);border:2px solid var(--amber);border-radius:10px;padding:20px 24px;margin-bottom:32px}}
.bottom-line-label{{font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--amber);letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px}}
.bottom-line-text{{font-size:15px;color:var(--ink);line-height:1.7;font-weight:500}}
.pros-cons{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:20px 0}}
.pros,.cons{{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:18px}}
.pros h4{{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:14px;color:var(--green);letter-spacing:0.08em;text-transform:uppercase;margin-bottom:12px}}
.cons h4{{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:14px;color:var(--red);letter-spacing:0.08em;text-transform:uppercase;margin-bottom:12px}}
.pros li,.cons li{{font-size:13px;color:var(--ink2);margin-bottom:8px;list-style:none;padding-left:18px;position:relative;line-height:1.5}}
.pros li::before{{content:'✓';position:absolute;left:0;color:var(--green);font-weight:700}}
.cons li::before{{content:'✗';position:absolute;left:0;color:var(--red);font-weight:700}}
.spec-table{{width:100%;border-collapse:collapse;margin:20px 0;background:var(--surface);border:1px solid var(--border);border-radius:10px;overflow:hidden}}
.spec-table tr{{border-bottom:1px solid var(--border2)}}
.spec-table tr:last-child{{border-bottom:none}}
.spec-table td{{padding:11px 16px;font-size:13px}}
.spec-table td:first-child{{font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--ink3);letter-spacing:0.05em;background:var(--bg);width:40%}}
.spec-table td:last-child{{font-weight:500;color:var(--ink)}}
.spec-highlight{{color:var(--green)!important;font-weight:700!important}}
.who-box{{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:20px;margin:20px 0}}
.who-box h4{{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:14px;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:10px}}
.faq-item{{border-bottom:1px solid var(--border);padding:16px 0}}
.faq-item:last-child{{border-bottom:none}}
.faq-q{{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:17px;color:var(--ink);cursor:pointer;display:flex;justify-content:space-between;align-items:center}}
.faq-a{{font-size:14px;color:var(--ink2);line-height:1.6;margin-top:10px;display:none}}
.faq-a.open{{display:block}}
.sidebar{{position:sticky;top:72px}}
.mid-cta{{background:var(--steel);border-radius:10px;padding:24px;margin:32px 0;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px}}
.mid-cta-title{{font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:22px;color:#fff;text-transform:uppercase}}
.mid-cta-price{{font-family:'Barlow Condensed',sans-serif;font-weight:900;font-size:28px;color:var(--amber2)}}
footer{{background:var(--steel);padding:28px 40px;margin-top:48px}}
.foot-inner{{max-width:1100px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px}}
.foot-logo{{font-family:'Barlow Condensed',sans-serif;font-weight:900;font-size:22px;color:#fff}}
.foot-logo em{{color:var(--amber2);font-style:normal}}
.foot-disc{{font-size:12px;color:rgba(255,255,255,0.25);max-width:500px;line-height:1.5}}
@media(max-width:768px){{
  .review-body{{grid-template-columns:1fr}}
  .hero-layout{{grid-template-columns:1fr}}
  .sidebar{{position:static}}
  .pros-cons{{grid-template-columns:1fr}}
  h1{{font-size:32px}}
  .review-hero{{padding:32px 16px 0}}
  .breadcrumb{{padding:10px 16px}}
  .review-body{{padding:32px 16px}}
  nav .nav-links,.nav-btn{{display:none}}
}}
</style>
</head>
<body>

{nav_html}
{mobile_html}
{search_html}

<div class="breadcrumb">
  <a href="/">Home</a> / 
  <a href="/{category}/">{category.replace('-',' ').title()}</a> / 
  {name[:60]}
</div>

<div class="review-hero">
  <div class="review-hero-inner">
    <div class="review-tag">Independent Review · Updated June 2026</div>
    <div class="hero-layout">
      <div class="hero-left">
        <h1>{name}</h1>
        <p class="tagline">{content.get('tagline', '')}</p>
        <div class="score-box">
          <div class="score-overall">
            <div class="score-num-big">{overall}</div>
            <div class="score-label-big">IndustrialRank Score</div>
          </div>
          <div class="score-row"><span class="score-label-s">Efficiency</span><div class="score-bar-wrap">{score_bar(ir.get('efficiency',8.0))}<span class="score-num">{ir.get('efficiency',8.0)}</span></div></div>
          <div class="score-row"><span class="score-label-s">Reliability</span><div class="score-bar-wrap">{score_bar(ir.get('reliability',8.0))}<span class="score-num">{ir.get('reliability',8.0)}</span></div></div>
          <div class="score-row"><span class="score-label-s">Value</span><div class="score-bar-wrap">{score_bar(ir.get('value',8.0))}<span class="score-num">{ir.get('value',8.0)}</span></div></div>
          <div class="score-row"><span class="score-label-s">Installation</span><div class="score-bar-wrap">{score_bar(ir.get('installation',8.0))}<span class="score-num">{ir.get('installation',8.0)}</span></div></div>
          <div class="score-row"><span class="score-label-s">Warranty</span><div class="score-bar-wrap">{score_bar(ir.get('warranty',8.0))}<span class="score-num">{ir.get('warranty',8.0)}</span></div></div>
        </div>
      </div>
      <div class="hero-right">
        <div class="hero-img">
          <img src="{image}" alt="{name}" loading="lazy" referrerpolicy="no-referrer">
        </div>
        <div class="buy-box">
          <div style="font-size:11px;color:var(--ink3);text-transform:uppercase;letter-spacing:.06em">Current Price</div>
          <div class="price-range">{price}</div>
          <a href="{aff_url}" target="_blank" rel="noopener sponsored" class="buy-btn">Check Price at HVACDirect →</a>
          <a href="{aff_url}" target="_blank" rel="noopener sponsored" class="buy-btn-sec">Shop Now at HVACDirect</a>
          <div style="font-size:11px;color:var(--ink3);margin-top:10px;text-align:center">Authorized dealer · Full manufacturer warranty</div>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="review-body">
  <div class="content">
    
    <div class="bottom-line-box">
      <div class="bottom-line-label">// Bottom Line</div>
      <div class="bottom-line-text">{content.get('bottom_line', '')}</div>
    </div>

    <h2>Review</h2>
    <p>{content.get('review_p1', '')}</p>
    <p>{content.get('review_p2', '')}</p>

    <h2>Pros &amp; Cons</h2>
    <div class="pros-cons">
      <div class="pros"><h4>Pros</h4><ul>{pros_html}</ul></div>
      <div class="cons"><h4>Cons</h4><ul>{cons_html}</ul></div>
    </div>

    <h2>Who Should Buy</h2>
    <div class="who-box">
      <h4 style="color:var(--green)">Best For</h4>
      <p style="font-size:14px;color:var(--ink2);margin:0">{content.get('who_should_buy', '')}</p>
    </div>
    <div class="who-box">
      <h4 style="color:var(--red)">Consider Alternatives If</h4>
      <p style="font-size:14px;color:var(--ink2);margin:0">{content.get('who_should_avoid', '')}</p>
    </div>

    <div class="mid-cta">
      <div>
        <div class="mid-cta-title">{name[:50]}</div>
        <div class="mid-cta-price">{price}</div>
      </div>
      <a href="{aff_url}" target="_blank" rel="noopener sponsored" class="buy-btn" style="width:auto;padding:14px 28px">Buy at HVACDirect →</a>
    </div>

    <h2>Installation</h2>
    <p>{content.get('install_section', '')}</p>

    <h2>Warranty &amp; Reliability</h2>
    <p>{content.get('warranty_section', '')}</p>

    <h2>Specifications</h2>
    <table class="spec-table">
      <tbody>{spec_rows}</tbody>
    </table>

    <h2>Frequently Asked Questions</h2>
    {faq_html}

    <div style="background:var(--amber-bg);border:1px solid var(--amber);border-radius:10px;padding:20px 24px;margin-top:32px;text-align:center">
      <p style="font-size:13px;color:var(--ink3);margin:0">Affiliate disclosure: IndustrialRank earns a commission on qualifying purchases at no extra cost to you. We only recommend products we have independently reviewed.</p>
    </div>

  </div>

  <div class="sidebar">
    <div class="buy-box">
      <div style="font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:18px;text-transform:uppercase;color:var(--ink);margin-bottom:4px">Buy This Product</div>
      <div style="font-size:11px;color:var(--ink3);margin-bottom:12px">Available at HVACDirect</div>
      <div class="price-range" style="font-size:28px">{price}</div>
      <a href="{aff_url}" target="_blank" rel="noopener sponsored" class="buy-btn">Check Price →</a>
      <a href="{aff_url}" target="_blank" rel="noopener sponsored" class="buy-btn-sec">View on HVACDirect</a>
      <div style="font-size:11px;color:var(--ink3);margin-top:10px;text-align:center">Free shipping on orders $2,000+</div>
    </div>
    <div style="background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:16px;margin-top:16px">
      <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--ink3);letter-spacing:.08em;text-transform:uppercase;margin-bottom:12px">Quick Specs</div>
      <table class="spec-table" style="margin:0">
        <tbody>
          {''.join(f'<tr><td>{k}</td><td>{v}</td></tr>' for k,v in list(specs.items())[:8])}
        </tbody>
      </table>
    </div>
  </div>
</div>

<footer>
  <div class="foot-inner">
    <div class="foot-logo">Industrial<em>Rank</em></div>
    <div class="foot-disc">Independent industrial equipment reviews. IndustrialRank is not affiliated with HVACDirect or any manufacturer. We earn affiliate commissions on qualifying purchases.</div>
  </div>
</footer>

<script>
document.querySelectorAll('.faq-q').forEach(q => {{
  q.addEventListener('click', () => {{
    const a = q.nextElementSibling;
    a.classList.toggle('open');
    q.querySelector('span').textContent = a.classList.contains('open') ? '−' : '+';
  }});
}});
</script>

</body>
</html>'''

if __name__ == '__main__':
    import sys
    test_url = 'https://hvacdirect.com/mrcool-diy-5th-gen-e-star-12000-btu-single-zone-mini-split-complete-system-with-25ft-line-set-115v-diy-12-hp-wm-115d25-o.html'
    cat = 'mini-splits'
    
    print("Nav HTML cekiliyor...")
    nav_html, mobile_html, search_html = get_nav()
    
    print("Urun scrape ediliyor...")
    product = scrape_product(test_url)
    if not product:
        print("HATA: Urun scrape edilemedi")
        sys.exit(1)
    print(f"Ad: {product['name']}")
    print(f"Fiyat: {product['price']}")
    print(f"Spec: {len(product['specs'])} adet")
    
    print("Claude API ile icerik uretiliyor...")
    content = generate_content(product)
    if not content:
        print("HATA: Icerik uretimi basarisiz")
        sys.exit(1)
    print(f"Tagline: {content.get('tagline','')}")
    
    slug = test_url.split('/')[-1].replace('.html','')
    out = PUBLIC / cat / slug / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    
    html = build_page(product, content, cat, nav_html, mobile_html, search_html)
    out.write_text(html, encoding='utf-8')
    print(f"\nSayfa yazildi: {out}")
    print("Tarayicida ac: open " + str(out))
