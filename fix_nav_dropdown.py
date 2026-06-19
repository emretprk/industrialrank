#!/usr/bin/env python3
"""
Fixes the overlapping nav-dropdown issue on the 8 category pages.
The category pages were regenerated with a copy of the nav HTML but not
the CSS that hides dropdowns until hover (.dropdown{display:none} etc).
This injects that missing CSS block right before </style> on each page.
"""

from pathlib import Path

PUBLIC = Path(__file__).parent / 'public'

CATEGORIES = ['heat-pumps', 'air-conditioners', 'mini-splits', 'electrical',
              'pumps', 'commercial-hvac', 'water-heating', 'air-quality']

MEGA_MENU_CSS = """
/* MEGA MENU */
.has-dropdown{position:relative}
.has-dropdown>a{cursor:default}
.has-dropdown>a::after{content:'\u25be';font-size:9px;margin-left:4px;opacity:0.5}
.dropdown{display:none;position:absolute;top:56px;left:0;background:var(--steel);border-top:3px solid var(--amber);box-shadow:0 16px 40px rgba(0,0,0,0.4);min-width:720px;padding:24px 0;z-index:200;border-radius:0 0 8px 8px}
.has-dropdown:hover .dropdown{display:flex}
.dropdown-col{flex:1;padding:0 24px;border-right:1px solid rgba(255,255,255,0.07)}
.dropdown-col:last-child{border-right:none}
.dropdown-col-title{font-family:'IBM Plex Mono',monospace;font-size:9px;color:var(--amber);letter-spacing:0.14em;text-transform:uppercase;margin-bottom:14px;padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,0.08)}
.dropdown-col a{display:block;font-size:12px;color:rgba(255,255,255,0.65);text-decoration:none;padding:6px 0;letter-spacing:0.02em;border-bottom:none;height:auto;text-transform:none;font-weight:400;transition:color 0.12s}
.dropdown-col a:hover{color:var(--amber2);border-bottom:none}
.dropdown-col a strong{display:block;color:rgba(255,255,255,0.9);font-weight:600;font-size:12px;margin-bottom:1px}
.dropdown-col a span{font-size:11px;color:rgba(255,255,255,0.35)}
.dropdown-footer{padding:14px 24px 0;border-top:1px solid rgba(255,255,255,0.07);display:flex;gap:12px;margin:16px 24px 0}
.dropdown-footer a{font-size:11px;color:var(--amber);text-decoration:none;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;height:auto;padding:0;border-bottom:none}
"""

fixed = 0
for cat in CATEGORIES:
    f = PUBLIC / cat / 'index.html'
    if not f.exists():
        continue
    html = f.read_text(encoding='utf-8')
    if '.dropdown{display:none' in html:
        print(f"{cat}: already has dropdown CSS, skipping")
        continue
    if '</style>' not in html:
        print(f"{cat}: WARNING no </style> tag found, skipping")
        continue
    html = html.replace('</style>', MEGA_MENU_CSS + '</style>', 1)
    f.write_text(html, encoding='utf-8')
    fixed += 1
    print(f"{cat}: dropdown CSS injected")

print(f"\nDone. {fixed} category pages fixed.")
