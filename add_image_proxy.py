#!/usr/bin/env python3
"""
Rewrites every <img src="https://hvacdirect.com/media/...."> reference
across all generated pages (and the search modal JS) to go through our
own /img?u=... proxy instead of hotlinking hvacdirect.com directly.

Does NOT touch the affiliate purchase links (hvacdirect.com/...html?affiliate_code=...)
— only image src attributes pointing at /media/ paths.
"""

import re
from pathlib import Path
from urllib.parse import quote

PUBLIC = Path(__file__).parent / 'public'

IMG_SRC_RE = re.compile(r'src="(https://hvacdirect\.com/media/[^"]*)"')

def proxy_replace(match):
    original = match.group(1)
    return f'src="/img?u={quote(original, safe="")}"'

files_changed = 0
total_replacements = 0

for f in PUBLIC.rglob('*.html'):
    html = f.read_text(encoding='utf-8')
    new_html, n = IMG_SRC_RE.subn(proxy_replace, html)

    # Also patch the search-modal JS that builds <img> tags from p.image
    # at render time (only present in index.html + 8 category pages).
    if "src=\"'+p.image+'\"" in new_html:
        new_html = new_html.replace(
            "src=\"'+p.image+'\"",
            "src=\"/img?u='+encodeURIComponent(p.image)+'\""
        )
        n += 1

    if n > 0:
        f.write_text(new_html, encoding='utf-8')
        files_changed += 1
        total_replacements += n

print(f"Done. {files_changed} files changed, {total_replacements} image references proxied.")
