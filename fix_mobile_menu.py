#!/usr/bin/env python3
"""
Adds the missing hamburger/mobile-menu CSS to the 8 category pages.
(The dropdown CSS was already fixed separately — this only adds what's
still missing: the rules that keep the mobile slide-out menu hidden
until the hamburger icon is tapped.)
"""

from pathlib import Path

PUBLIC = Path(__file__).parent / 'public'

CATEGORIES = ['heat-pumps', 'air-conditioners', 'mini-splits', 'electrical',
              'pumps', 'commercial-hvac', 'water-heating', 'air-quality']

MOBILE_MENU_CSS = """
/* MOBILE MENU / HAMBURGER */
.hamburger{display:none;flex-direction:column;gap:5px;cursor:pointer;padding:8px;background:none;border:none}
.hamburger span{display:block;width:22px;height:2px;background:#fff;border-radius:2px;transition:all 0.3s}
.hamburger.open span:nth-child(1){transform:rotate(45deg) translate(5px,5px)}
.hamburger.open span:nth-child(2){opacity:0}
.hamburger.open span:nth-child(3){transform:rotate(-45deg) translate(5px,-5px)}
.mobile-menu{display:none;position:fixed;top:56px;left:0;right:0;background:var(--steel);border-top:1px solid rgba(255,255,255,0.1);padding:16px 24px;z-index:99;flex-direction:column;gap:0}
.mobile-menu a{color:rgba(255,255,255,0.7);text-decoration:none;font-size:14px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;padding:14px 0;border-bottom:1px solid rgba(255,255,255,0.06);display:block}
.mobile-menu a:last-child{border-bottom:none}
.mobile-menu.open{display:flex}
@media(max-width:768px){.hamburger{display:none}nav{flex-wrap:wrap;height:auto;padding:10px 16px;gap:8px}.logo{width:100%}.nav-links{width:100%;overflow-x:auto;padding-bottom:6px;scrollbar-width:none;gap:0}.nav-links::-webkit-scrollbar{display:none}.nav-links a{font-size:11px;padding:0 10px;white-space:nowrap}.nav-btn{display:none}}
"""

fixed = 0
for cat in CATEGORIES:
    f = PUBLIC / cat / 'index.html'
    if not f.exists():
        continue
    html = f.read_text(encoding='utf-8')
    if '.mobile-menu{display:none' in html:
        print(f"{cat}: already has mobile-menu CSS, skipping")
        continue
    if '</style>' not in html:
        print(f"{cat}: WARNING no </style> tag found, skipping")
        continue
    html = html.replace('</style>', MOBILE_MENU_CSS + '</style>', 1)
    f.write_text(html, encoding='utf-8')
    fixed += 1
    print(f"{cat}: mobile-menu CSS injected")

print(f"\nDone. {fixed} category pages fixed.")
