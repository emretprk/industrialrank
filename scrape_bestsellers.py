#!/usr/bin/env python3
"""
Scrapes HVACDirect category listing pages and ranks products by review
count (a reliable popularity/bestseller proxy — HVACDirect's own "Best
Sellers" sort toggle didn't respond to a URL parameter, but review count
is visible directly on every listing page and correlates with sales).

Writes bestseller_urls.txt: one URL per line, grouped by category,
ordered by review count descending within each category.

Run locally (needs real internet access to hvacdirect.com):
    python3 scrape_bestsellers.py
"""

import re
import time
import requests
from collections import defaultdict
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Referer': 'https://www.google.com/',
}

# Seed category listing pages per IndustrialRank category. Some of these
# are flat product grids (ideal); a few may be "hub" pages that mostly
# link to sub-categories rather than products directly — the scraper
# will print a low-yield warning for those so you can swap in a more
# specific sub-category URL if needed.
SEEDS = {
    'air-conditioners': [
        'https://hvacdirect.com/air-conditioner-condensers.html',
        'https://hvacdirect.com/air-conditioning-systems.html',
    ],
    'heat-pumps': [
        'https://hvacdirect.com/heat-pump-condensers-ac.html',
        'https://hvacdirect.com/heat-pump-systems.html',
    ],
    'mini-splits': [
        'https://hvacdirect.com/ductless-mini-splits/single-zone-ductless-mini-splits.html',
        'https://hvacdirect.com/ductless-mini-splits/dual-zone-ductless-mini-split-systems.html',
    ],
    'furnaces': [
        'https://hvacdirect.com/furnaces.html',
    ],
    'commercial-hvac': [
        'https://hvacdirect.com/commercial-hvac-equipment.html',
    ],
    'ventilation': [
        'https://hvacdirect.com/ventilation-products/residential-fans.html',
        'https://hvacdirect.com/ventilation-products/rooftop-fans.html',
    ],
    'air-quality': [
        'https://hvacdirect.com/air-cleaning.html',
    ],
}

MAX_PAGES_PER_SEED = 5   # paginate ?p=2, ?p=3 ... up to this many pages
PER_CATEGORY_TARGET = 200  # stop once we have this many candidates for a category

PRODUCT_URL_RE = re.compile(r'^https://hvacdirect\.com/[a-z0-9\-]+\.html$', re.IGNORECASE)

NON_PRODUCT_SUFFIXES = (
    '-systems.html', '-conditioners.html', '-condensers.html', '-pumps.html',
    '-units.html', '-equipment.html', '-products.html', '-fans.html',
    '-furnaces.html', '-splits.html', '-cleaning.html', '-accessories.html',
    '-handlers.html', '-heaters.html',
)

ALL_SEED_URLS = {u for seeds in SEEDS.values() for u in seeds}

def looks_like_product(url):
    if not PRODUCT_URL_RE.match(url):
        return False
    if url in ALL_SEED_URLS:
        return False
    if '/filter/' in url:
        return False
    path = url.rsplit('/', 1)[-1]
    if path.lower().endswith(NON_PRODUCT_SUFFIXES) and len(path) < 45:
        return False
    if len(path) < 25:
        return False
    return True


def scrape_listing_page(url):
    """Returns list of (product_url, review_count) found on one listing page."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            return []
    except Exception as e:
        print(f"    fetch failed: {e}")
        return []

    soup = BeautifulSoup(r.text, 'html.parser')
    results = []
    seen = set()

    # Product cards are typically <li class="item product product-item"> in Magento
    for link in soup.find_all('a', href=True):
        href = link['href'].split('?')[0]
        if not looks_like_product(href) or href in seen:
            continue
        seen.add(href)

        # Look for a review count near this link (within the same product card)
        review_count = 0
        card = link
        for _ in range(6):
            card = card.parent
            if card is None:
                break
            text = card.get_text(' ', strip=True)
            m = re.search(r'(\d+)\s+Review', text)
            if m:
                review_count = int(m.group(1))
                break

        results.append((href, review_count))

    return results


def main():
    all_candidates = defaultdict(dict)  # cat -> {url: review_count}

    for cat, seeds in SEEDS.items():
        print(f"\n=== {cat} ===")
        for seed in seeds:
            for page in range(1, MAX_PAGES_PER_SEED + 1):
                url = seed if page == 1 else f"{seed}?p={page}"
                found = scrape_listing_page(url)
                if not found:
                    break
                for product_url, reviews in found:
                    if product_url not in all_candidates[cat] or reviews > all_candidates[cat][product_url]:
                        all_candidates[cat][product_url] = reviews
                print(f"  {url} -> {len(found)} products found")
                time.sleep(0.5)
                if len(all_candidates[cat]) >= PER_CATEGORY_TARGET:
                    break
            if len(all_candidates[cat]) >= PER_CATEGORY_TARGET:
                break

        n = len(all_candidates[cat])
        if n < 10:
            print(f"  WARNING: only {n} products found for {cat} — seed URL may be a hub page, not a flat listing. Check manually.")
        else:
            print(f"  Total for {cat}: {n}")

    with open('bestseller_urls.txt', 'w') as f:
        for cat, products in all_candidates.items():
            ranked = sorted(products.items(), key=lambda x: -x[1])
            for url, reviews in ranked:
                f.write(f"{url}\n")

    total = sum(len(v) for v in all_candidates.values())
    print(f"\nDone. {total} bestseller-ranked URLs written to bestseller_urls.txt")


if __name__ == '__main__':
    main()
