#!/usr/bin/env python3
"""
generate_search_index.py
Tüm ürün sayfalarını tarayıp /public/search-index.json üretir.

Kullanım:
  python3 generate_search_index.py

Çalıştırma yeri: ~/Downloads/industrialrank/
"""

import os
import re
import json
from pathlib import Path

PUBLIC_DIR = Path("public")
OUTPUT = PUBLIC_DIR / "search-index.json"

PRODUCT_DIRS = [
    "mini-splits",
    "heat-pumps",
    "air-conditioners",
    "pumps",
    "commercial-hvac",
    "water-heating",
    "air-quality",
]

def extract(html, pattern, default=""):
    m = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
    return m.group(1).strip() if m else default

def parse_price(text):
    m = re.search(r'\$([0-9,]+)', text)
    if m:
        try:
            return int(m.group(1).replace(",", ""))
        except:
            pass
    return None

def get_category(path):
    parts = path.parts
    for p in PRODUCT_DIRS:
        if p in parts:
            return p.replace("-", " ").title()
    return ""

def process_file(html_path):
    try:
        html = html_path.read_text(encoding="utf-8", errors="ignore")
    except:
        return None

    if len(html) < 5000:
        return None

    name = extract(html, r'<title>([^<|]+)')
    name = re.sub(r'\s*[-|]\s*IndustrialRank.*$', '', name).strip()
    if not name:
        return None

    brand = extract(html, r'<meta[^>]+name=["\']brand["\'][^>]+content=["\']([^"\']+)')
    if not brand:
        brand = extract(html, r'class="brand[^"]*">([^<]+)')
    if not brand:
        brand = name.split()[0] if name else ""

    price_text = extract(html, r'class="[^"]*price[^"]*">([^<]+)')
    price = parse_price(price_text)

    img = extract(html, r'<img[^>]+class="[^"]*product[^"]*"[^>]+src=["\']([^"\']+)')
    if not img:
        img = extract(html, r'<img[^>]+src=["\']([^"\']+(?:jpg|jpeg|png|webp)[^"\']*)["\']')

    rel = html_path.relative_to(PUBLIC_DIR)
    parts = rel.parts
    if parts[-1] == "index.html":
        url = "/" + "/".join(parts[:-1]) + "/"
    else:
        url = "/" + "/".join(parts)

    cat = get_category(html_path)

    return {"n": name, "b": brand, "cat": cat, "price": price, "img": img, "url": url}

def main():
    products = []
    scanned = 0
    skipped = 0

    for cat_dir in PRODUCT_DIRS:
        cat_path = PUBLIC_DIR / cat_dir
        if not cat_path.exists():
            print(f"  Klasor yok: {cat_dir}, atlaniyor")
            continue

        html_files = list(cat_path.rglob("index.html"))
        print(f"  {cat_dir}: {len(html_files)} dosya taraniyor...")

        for f in html_files:
            scanned += 1
            result = process_file(f)
            if result:
                products.append(result)
            else:
                skipped += 1

    print(f"\nToplam: {scanned} dosya, {len(products)} urun indexlendi, {skipped} atlandi")

    OUTPUT.write_text(json.dumps(products, separators=(',', ':')), encoding="utf-8")
    size_kb = OUTPUT.stat().st_size / 1024
    print(f"Yazildi: {OUTPUT} ({size_kb:.1f} KB)")
    if products:
        print(f"Ornek: {products[0]}")

if __name__ == "__main__":
    main()
