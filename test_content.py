#!/usr/bin/env python3
"""
IndustrialRank - Ürün Sayfası İçerik Üretici
HVACDirect'ten spec çeker, Claude API ile içerik üretir.
"""

import requests
import json
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Referer': 'https://www.google.com/'
}
AFF_CODE = '?affiliate_code=Ob419ERXae&referring_service=link'

def scrape_product(url):
    r = requests.get(url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    name = soup.find('h1')
    price = soup.find('meta', property='product:price:amount')
    image = soup.find('meta', property='og:image')
    
    specs = {}
    for row in soup.find_all('tr'):
        cols = row.find_all(['td', 'th'])
        if len(cols) >= 2:
            key = cols[0].text.strip()
            val = cols[1].text.strip()
            if key and len(key) < 50:
                specs[key] = val
    
    return {
        'name': name.text.strip() if name else '',
        'price': '$' + price['content'] if price else '',
        'image': image['content'] if image else '',
        'url': url,
        'aff_url': url + AFF_CODE,
        'specs': specs
    }

def generate_content(product):
    prompt = f"""You are writing a product review for IndustrialRank, an independent HVAC equipment review site.

Product: {product['name']}
Price: {product['price']}
Specs:
{json.dumps(product['specs'], indent=2)}

Write a comprehensive product review with these sections. Be specific, data-driven, and helpful. Do NOT use em dashes (—). Use commas or restructure sentences instead.

Return ONLY valid JSON with these exact keys:
{{
  "tagline": "One sentence that captures the product's key value proposition (under 15 words)",
  "bottom_line": "2-3 sentence summary of who this product is best for and why",
  "pros": ["pro 1", "pro 2", "pro 3", "pro 4", "pro 5"],
  "cons": ["con 1", "con 2", "con 3"],
  "who_should_buy": "2 sentences about ideal buyer profile",
  "who_should_avoid": "1 sentence about who should look elsewhere",
  "review_intro": "2 paragraph introduction to the product (150-200 words total)",
  "efficiency_section": "1 paragraph about efficiency and energy performance (80-100 words)",
  "installation_section": "1 paragraph about installation requirements (80-100 words)",
  "warranty_section": "1 paragraph about warranty and reliability (60-80 words)",
  "faq": [
    {{"q": "question 1", "a": "answer 1"}},
    {{"q": "question 2", "a": "answer 2"}},
    {{"q": "question 3", "a": "answer 3"}},
    {{"q": "question 4", "a": "answer 4"}},
    {{"q": "question 5", "a": "answer 5"}}
  ]
}}"""

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"Content-Type": "application/json", "x-api-key": "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", "anthropic-version": "2023-06-01"},
        json={
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 2000,
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=30
    )
    
    data = response.json()
    text = data['content'][0]['text']
    
    # JSON parse
    text = text.strip()
    if text.startswith('```'):
        text = text.split('```')[1]
        if text.startswith('json'):
            text = text[4:]
    
    return json.loads(text.strip())

# Test
url = 'https://hvacdirect.com/mrcool-diy-5th-gen-e-star-12000-btu-single-zone-mini-split-complete-system-with-25ft-line-set-115v-diy-12-hp-wm-115d25-o.html'
print("Scraping...")
product = scrape_product(url)
print(f"Ad: {product['name']}")
print(f"Fiyat: {product['price']}")
print(f"Spec sayisi: {len(product['specs'])}")

print("\nClaude API ile icerik uretiliyor...")
content = generate_content(product)
print(f"Tagline: {content['tagline']}")
print(f"Bottom line: {content['bottom_line'][:100]}...")
print(f"Pros: {len(content['pros'])} adet")
print(f"FAQ: {len(content['faq'])} soru")
print("\nTEST BASARILI!")
