#!/usr/bin/env python3
"""
IndustrialRank - HVACDirect Görsel Ekleyici
Her ürün sayfasındaki HVACDirect URL'sini bulur, görseli çeker, HTML'e ekler.
"""

import os
import re
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://www.google.com/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

def get_hvacdirect_image(product_url):
    """HVACDirect ürün sayfasından ana görseli çek."""
    try:
        r = requests.get(product_url, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.text, "html.parser")

        # Ana ürün görseli — genellikle .main-image, #main-product-image, veya og:image
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]

        img = soup.select_one(".product-image-main img, #main-image img, .main-image img")
        if img and img.get("src"):
            src = img["src"]
            if src.startswith("//"):
                src = "https:" + src
            return src

        return None
    except Exception as e:
        print(f"  Hata: {e}")
        return None

def extract_hvacdirect_url(html_content):
    """HTML'den HVACDirect ürün URL'sini çıkar (affiliate linkten önce)."""
    match = re.search(r'href="(https://hvacdirect\.com/[^"]+\.html[^"]*)"', html_content)
    if match:
        url = match.group(1)
        # Affiliate parametresiz temiz URL
        base_url = url.split("?")[0]
        return base_url
    return None

def inject_image(html_content, image_url, alt_text="Product Image"):
    """HTML'e görsel ekle — hero bölümünün içine."""
    img_tag = f'<div class="product-hero-img" style="text-align:center;margin:24px 0;"><img src="{image_url}" alt="{alt_text}" style="max-width:100%;max-height:480px;object-fit:contain;border-radius:8px;" loading="lazy" referrerpolicy="no-referrer"></div>'

    # <h1> tag'inden önce ekle
    if "<h1" in html_content:
        html_content = html_content.replace("<h1", img_tag + "\n<h1", 1)
        return html_content

    return None

def process_file(filepath, dry_run=False):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Zaten görsel var mı?
    if "product-hero-img" in content:
        return "skip"

    hvacdirect_url = extract_hvacdirect_url(content)
    if not hvacdirect_url:
        return "no_url"

    print(f"  Fetching: {hvacdirect_url}")
    image_url = get_hvacdirect_image(hvacdirect_url)
    if not image_url:
        return "no_image"

    # Alt text için başlık çek
    title_match = re.search(r"<title>([^<]+)</title>", content)
    alt_text = title_match.group(1).split("|")[0].strip() if title_match else "Product"

    new_content = inject_image(content, image_url, alt_text)
    if not new_content:
        return "inject_failed"

    if not dry_run:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

    print(f"  Gorsel eklendi: {image_url[:80]}...")
    return "ok"

def main(public_dir, limit=None, dry_run=False):
    public_path = Path(public_dir)
    html_files = list(public_path.rglob("index.html"))

    # Ana sayfa ve kategori index'lerini atla (küçük dosyalar)
    product_files = [f for f in html_files if f.stat().st_size > 20000]

    if limit:
        product_files = product_files[:limit]

    print(f"Toplam {len(product_files)} ürün sayfası işlenecek")
    print(f"Dry run: {dry_run}\n")

    stats = {"ok": 0, "skip": 0, "no_url": 0, "no_image": 0, "inject_failed": 0}

    for i, filepath in enumerate(product_files, 1):
        print(f"[{i}/{len(product_files)}] {filepath.parent.name}/")
        result = process_file(filepath, dry_run=dry_run)
        stats[result] = stats.get(result, 0) + 1
        if result == "ok":
            time.sleep(0.5)  # Rate limit için bekle

    print(f"\n{'='*50}")
    print(f"TAMAMLANDI")
    print(f"  Gorsel eklendi : {stats['ok']}")
    print(f"  Zaten vardı    : {stats['skip']}")
    print(f"  URL yok        : {stats['no_url']}")
    print(f"  Gorsel bulunamadı: {stats['no_image']}")
    print(f"{'='*50}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="./public", help="Public dizini")
    parser.add_argument("--limit", type=int, default=None, help="Test için limit")
    parser.add_argument("--dry-run", action="store_true", help="Dosya yazma")
    args = parser.parse_args()
    main(args.dir, args.limit, args.dry_run)
