#!/usr/bin/env python3
"""
Fixes 38 broken nav mega-menu product links spread across 13 info/blog pages
(about, contact, privacy-policy, blog index + 5 posts, top10, compare, find, hvac).

Root cause: the mega-menu was hand-authored during the category restructure
with placeholder/example products that were never cross-checked against the
real built catalog. Every single specific-product link in it was fake.

Fix strategy:
- Categories WITH real inventory (heat-pumps, air-conditioners, mini-splits):
  swap the fake entries for real products pulled from public/<category>/.
- Categories WITH ZERO real inventory (electrical, pumps, water-heating,
  air-quality, commercial-hvac): drop the fake product columns entirely and
  keep only a "Resources" column pointing at links we've verified exist.

Run from the repo root: python3 fix_megamenu_404s.py
"""

from pathlib import Path

PUBLIC = Path(__file__).parent / "public"

AFFECTED_FILES = [
    "about/index.html",
    "contact/index.html",
    "privacy-policy/index.html",
    "find/index.html",
    "compare/index.html",
    "top10/index.html",
    "hvac/index.html",
    "blog/index.html",
    "blog/industrial-electrical-trends-2026/index.html",
    "blog/industrial-pump-technology-2026/index.html",
    "blog/hvac-technologies-2026/index.html",
    "blog/compressed-air-systems-2026/index.html",
    "blog/industrial-automation-trends-2026/index.html",
]

# ---- OLD (broken) blocks, verbatim from the live HTML ----

OLD_HEAT_PUMPS = '''      <div class="dropdown">
        <div class="dropdown-col">
          <div class="dropdown-col-title">Variable-Speed</div>
          <a href="/heat-pumps/carrier-infinity-20-heat-pump-review/"><strong>Carrier Infinity 20</strong><span>20 SEER2 · Variable-speed</span></a>
          <a href="/heat-pumps/lennox-xp21-heat-pump-review/"><strong>Lennox XP21</strong><span>21.5 SEER2 · -13°F</span></a>
          <a href="/heat-pumps/bosch-bova-60hdn1-heat-pump-review/"><strong>Bosch IDS Premium</strong><span>20 SEER2 · Best value premium</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Standard Efficiency</div>
          <a href="/heat-pumps/trane-xr15-heat-pump-review/"><strong>Trane XR15</strong><span>17 SEER2 · Climatuff</span></a>
          <a href="/heat-pumps/goodman-gsx160481-heat-pump-review/"><strong>Goodman GSX16</strong><span>16 SEER2 · Best value</span></a>
          <a href="/heat-pumps/rheem-rp1648aj1na-heat-pump-review/"><strong>Rheem RP1648</strong><span>17 SEER2 · EcoNet WiFi</span></a>
          <a href="/heat-pumps/aciq-2ton-18seer2-heat-pump-review/"><strong>ACiQ 18 SEER2</strong><span>R-454B · 10-yr warranty</span></a>
          <a href="/heat-pumps/trane-runtru-2ton-heat-pump-review/"><strong>Trane RunTru</strong><span>14.3 SEER2 · Entry level</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Resources</div>
          <a href="/heat-pumps/">All Heat Pump Reviews →</a>
          <a href="/top10/">Top 10 Heat Pumps 2026</a>
          <a href="/blog/hvac-technologies-2026/">HVAC Technology Guide</a>
        </div>
      </div>'''

NEW_HEAT_PUMPS = '''      <div class="dropdown">
        <div class="dropdown-col">
          <div class="dropdown-col-title">Popular Reviews</div>
          <a href="/heat-pumps/1-5-ton-16-seer-goodman-heat-pump-gsz160181/"><strong>Goodman GSZ16</strong><span>1.5 Ton · 16 SEER</span></a>
          <a href="/heat-pumps/2-ton-17-5-seer-aciq-heat-pump-air-conditioner-system-id3448/"><strong>ACiQ Split System</strong><span>2 Ton · 17.5 SEER · Variable Speed</span></a>
          <a href="/heat-pumps/3-5-ton-13-4-seer2-multi-position-goodman-packaged-heat-pump-system-gphm34241/"><strong>Goodman GPHM34241</strong><span>3.5 Ton · 13.4 SEER2 · Packaged</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Resources</div>
          <a href="/heat-pumps/">All Heat Pump Reviews →</a>
          <a href="/top10/">Top 10 Heat Pumps 2026</a>
          <a href="/blog/hvac-technologies-2026/">HVAC Technology Guide</a>
        </div>
      </div>'''

OLD_MINI_SPLITS = '''      <div class="dropdown">
        <div class="dropdown-col">
          <div class="dropdown-col-title">DIY Systems</div>
          <a href="/mini-splits/mrcool-diy-24k-mini-split-review/"><strong>MRCOOL DIY 24K</strong><span>Pre-charged · No license needed</span></a>
          <a href="/mini-splits/mrcool-diy-36k-mini-split-review/"><strong>MRCOOL DIY 36K</strong><span>3-ton DIY · Large spaces</span></a>
          <a href="/mini-splits/mrcool-diy-2-zone-27k-review/"><strong>MRCOOL DIY 2-Zone</strong><span>Dual zone DIY</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Single Zone</div>
          <a href="/mini-splits/pioneer-wb009gmfi22m-mini-split-review/"><strong>Pioneer WB009 9K</strong><span>22 SEER · 22 dB</span></a>
          <a href="/mini-splits/senville-leto-12k-mini-split-review/"><strong>Senville LETO 12K</strong><span>19 SEER · 115V option</span></a>
          <a href="/mini-splits/lg-ls120hev2-mini-split-review/"><strong>LG Art Cool 12K</strong><span>27 SEER2 · Design panel</span></a>
          <a href="/mini-splits/cooper-hunter-sophia-24k-review/"><strong>Cooper &amp; Hunter 24K</strong><span>21 SEER · Best value 24K</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Multi Zone</div>
          <a href="/mini-splits/mitsubishi-mxz-3c24na-review/"><strong>Mitsubishi MXZ-3C24</strong><span>3-zone · Hyper-Heat</span></a>
          <a href="/mini-splits/mitsubishi-mxz-4c36na-mini-split-review/"><strong>Mitsubishi MXZ-4C36</strong><span>4-zone · 20 SEER</span></a>
          <a href="/mini-splits/pioneer-3-zone-27k-mini-split-review/"><strong>Pioneer 3-Zone 27K</strong><span>Best value 3-zone</span></a>
          <a href="/mini-splits/daikin-vrv5-review/"><strong>Daikin VRV 5</strong><span>Commercial VRF · 64 zones</span></a>
        </div>
      </div>'''

NEW_MINI_SPLITS = '''      <div class="dropdown">
        <div class="dropdown-col">
          <div class="dropdown-col-title">Popular Reviews</div>
          <a href="/mini-splits/15-000-btu-21-6-seer-wall-mounted-mitsubishi-mini-split-gs-single-zone-heat-pump-id8959/"><strong>Mitsubishi MZ-GS15NA</strong><span>15K BTU · 21.6 SEER · Single Zone</span></a>
          <a href="/mini-splits/daikin-21-000-btu-tri-zone-mini-split-system-7-7-7-id1521/"><strong>Daikin Tri-Zone</strong><span>24K BTU · 17 SEER · 3 Zone</span></a>
          <a href="/mini-splits/36-000-btu-17-seer-dual-zone-wall-mounted-daikin-mini-split-heat-pump-system-9-24-1519/"><strong>Daikin Dual-Zone</strong><span>36K BTU · 17 SEER · 2 Zone</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Resources</div>
          <a href="/mini-splits/">All Mini Split Reviews →</a>
          <a href="/top10/">Top 10 Mini Splits 2026</a>
        </div>
      </div>'''

OLD_AC = '''      <div class="dropdown">
        <div class="dropdown-col">
          <div class="dropdown-col-title">High Efficiency</div>
          <a href="/air-conditioners/lennox-xc21-air-conditioner-review/"><strong>Lennox XC21</strong><span>21 SEER2 · SilentComfort</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Value Tier</div>
          <a href="/air-conditioners/goodman-gsxh503610-ac-system-review/"><strong>Goodman GSXH5</strong><span>16 SEER2 · Lifetime compressor</span></a>
          <a href="/air-conditioners/carrier-performance-14-ac-review/"><strong>Carrier Performance 14</strong><span>15 SEER2 · Carrier network</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Resources</div>
          <a href="/air-conditioners/">All AC Reviews →</a>
          <a href="/compare/">Compare Models</a>
        </div>
      </div>'''

NEW_AC = '''      <div class="dropdown">
        <div class="dropdown-col">
          <div class="dropdown-col-title">Popular Reviews</div>
          <a href="/air-conditioners/2-5-ton-13-4-seer2-dedicated-horizontal-goodman-packaged-air-conditioner-gpch33041/"><strong>Goodman GPCH33041</strong><span>2.5 Ton · 13.4 SEER2 · Horizontal</span></a>
          <a href="/air-conditioners/2-5-ton-13-4-seer2-multi-position-goodman-packaged-air-conditioner-gpcm33041/"><strong>Goodman GPCM33041</strong><span>2.5 Ton · 13.4 SEER2 · Multi-Position</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Resources</div>
          <a href="/air-conditioners/">All AC Reviews →</a>
          <a href="/compare/">Compare Models</a>
        </div>
      </div>'''

OLD_ELECTRICAL = '''      <div class="dropdown">
        <div class="dropdown-col">
          <div class="dropdown-col-title">Panels &amp; Breakers</div>
          <a href="/electrical/eaton-br2020-review/"><strong>Eaton BR2020</strong><span>200A · 22kAIC · Load center</span></a>
          <a href="/electrical/siemens-q2200-review/"><strong>Siemens Q2200</strong><span>200A · 65kAIC · Main breaker</span></a>
          <a href="/electrical/square-d-hom2160pcvp-panel-review/"><strong>Square D HOM2160</strong><span>200A · 60-space · Value pack</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Test Equipment</div>
          <a href="/electrical/fluke-117-review/"><strong>Fluke 117</strong><span>True RMS · CAT III · VolT Alert</span></a>
          <a href="/electrical/fluke-323-clamp-meter-review/"><strong>Fluke 323</strong><span>400A clamp · True RMS</span></a>
          <a href="/electrical/klein-tools-mm400-multimeter-review/"><strong>Klein MM400</strong><span>True RMS · Best value</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Resources</div>
          <a href="/electrical/">All Electrical Reviews →</a>
          <a href="/blog/industrial-electrical-trends-2026/">Electrical Trends 2026</a>
        </div>
      </div>'''

NEW_ELECTRICAL = '''      <div class="dropdown">
        <div class="dropdown-col">
          <div class="dropdown-col-title">Resources</div>
          <a href="/electrical/">All Electrical Reviews →</a>
          <a href="/blog/industrial-electrical-trends-2026/">Electrical Trends 2026</a>
        </div>
      </div>'''

OLD_PUMPS = '''      <div class="dropdown">
        <div class="dropdown-col">
          <div class="dropdown-col-title">Process &amp; Industrial</div>
          <a href="/pumps/xylem-goulds-3196-review/"><strong>Xylem Goulds 3196</strong><span>ANSI B73.1 · Industry standard</span></a>
          <a href="/pumps/grundfos-cm5-5-review/"><strong>Grundfos CM5-5</strong><span>Multi-stage · 316SS</span></a>
          <a href="/pumps/grundfos-up15-29su-circulator-review/"><strong>Grundfos UP15-29SU</strong><span>Circulator · DHW/hydronic</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Sump &amp; Drainage</div>
          <a href="/pumps/zoeller-m53-sump-pump-review/"><strong>Zoeller M53</strong><span>Cast iron · Professional grade</span></a>
          <a href="/pumps/wayne-cdu980e-sump-pump-review/"><strong>Wayne CDU980E</strong><span>3/4 HP · 77 GPM</span></a>
          <a href="/pumps/little-giant-553271-sump-pump-review/"><strong>Little Giant 553271</strong><span>1/3 HP · Best value</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Resources</div>
          <a href="/pumps/">All Pump Reviews →</a>
          <a href="/blog/industrial-pump-technology-2026/">Pump Technology 2026</a>
        </div>
      </div>'''

NEW_PUMPS = '''      <div class="dropdown">
        <div class="dropdown-col">
          <div class="dropdown-col-title">Resources</div>
          <a href="/pumps/">All Pump Reviews →</a>
          <a href="/blog/industrial-pump-technology-2026/">Pump Technology 2026</a>
        </div>
      </div>'''

OLD_MORE = '''      <div class="dropdown">
        <div class="dropdown-col">
          <div class="dropdown-col-title">Air Quality</div>
          <a href="/air-quality/aprilaire-5000-whole-house-filter-review/"><strong>Aprilaire 5000</strong><span>MERV 16 whole-house</span></a>
          <a href="/air-quality/santa-fe-ultra120-dehumidifier-review/"><strong>Santa Fe Ultra120</strong><span>120 pt/day dehumidifier</span></a>
          <a href="/air-quality/aprilaire-8100-erv-review/"><strong>Aprilaire 8100 ERV</strong><span>Energy recovery ventilator</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Water Heating</div>
          <a href="/water-heating/aciq-50gal-hybrid-heat-pump-wh-review/"><strong>ACiQ 50-Gal HPWH</strong><span>3.75 UEF · IRA eligible</span></a>
          <a href="/water-heating/rinnai-rl75in-tankless-review/"><strong>Rinnai RL75iN</strong><span>7.5 GPM · 12-yr warranty</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Commercial HVAC</div>
          <a href="/commercial-hvac/carrier-50xp-packaged-heat-pump-review/"><strong>Carrier 50XP</strong><span>5-ton rooftop · BACnet</span></a>
          <a href="/commercial-hvac/reznor-udxc-unit-heater-review/"><strong>Reznor UDXC</strong><span>Unit heater · 20-yr warranty</span></a>
        </div>
      </div>'''

NEW_MORE = '''      <div class="dropdown">
        <div class="dropdown-col">
          <div class="dropdown-col-title">Coming Soon</div>
          <a href="/air-quality/">Air Quality →</a>
          <a href="/water-heating/">Water Heating →</a>
          <a href="/commercial-hvac/">Commercial HVAC →</a>
        </div>
      </div>'''

REPLACEMENTS = [
    (OLD_HEAT_PUMPS, NEW_HEAT_PUMPS, "heat-pumps"),
    (OLD_MINI_SPLITS, NEW_MINI_SPLITS, "mini-splits"),
    (OLD_AC, NEW_AC, "air-conditioners"),
    (OLD_ELECTRICAL, NEW_ELECTRICAL, "electrical"),
    (OLD_PUMPS, NEW_PUMPS, "pumps"),
    (OLD_MORE, NEW_MORE, "more/air-quality/water-heating/commercial-hvac"),
]

total_fixed = 0
for rel_path in AFFECTED_FILES:
    f = PUBLIC / rel_path
    if not f.exists():
        print(f"SKIP (not found): {rel_path}")
        continue
    html = f.read_text(encoding="utf-8")
    file_changes = 0
    for old, new, label in REPLACEMENTS:
        if old in html:
            html = html.replace(old, new, 1)
            file_changes += 1
    if file_changes:
        f.write_text(html, encoding="utf-8")
        total_fixed += file_changes
        print(f"{rel_path}: {file_changes} section(s) fixed")
    else:
        print(f"{rel_path}: no matching broken blocks found (check manually)")

print(f"\nDone. {total_fixed} mega-menu sections fixed across {len(AFFECTED_FILES)} files.")
