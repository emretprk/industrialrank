#!/usr/bin/env python3
"""Nav'daki alt kategori linklerini ana kategori sayfalarına yönlendir."""

import re

filepath = '/Users/emretoprak/Downloads/industrialrank/public/index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Mini Splits alt kategori linklerini düzelt
replacements = [
    # Mini Splits
    ('href="/mini-splits/diy/"', 'href="/mini-splits/"'),
    ('href="/mini-splits/single-zone/"', 'href="/mini-splits/"'),
    ('href="/mini-splits/multi-zone/"', 'href="/mini-splits/"'),
    ('href="/mini-splits/9000-btu/"', 'href="/mini-splits/"'),
    ('href="/mini-splits/12000-btu/"', 'href="/mini-splits/"'),
    ('href="/mini-splits/18000-btu/"', 'href="/mini-splits/"'),
    ('href="/mini-splits/24000-btu/"', 'href="/mini-splits/"'),
    # Heat Pumps
    ('href="/heat-pumps/air-source/"', 'href="/heat-pumps/"'),
    ('href="/heat-pumps/ground-source/"', 'href="/heat-pumps/"'),
    ('href="/heat-pumps/mini-split/"', 'href="/heat-pumps/"'),
    ('href="/heat-pumps/dual-fuel/"', 'href="/heat-pumps/"'),
    ('href="/brands/mitsubishi/"', 'href="/heat-pumps/"'),
    ('href="/brands/daikin/"', 'href="/heat-pumps/"'),
    ('href="/brands/carrier/"', 'href="/heat-pumps/"'),
    ('href="/brands/goodman/"', 'href="/heat-pumps/"'),
    # Air Conditioners
    ('href="/hvac/central-air/"', 'href="/hvac/"'),
    ('href="/hvac/window-units/"', 'href="/hvac/"'),
    ('href="/hvac/portable/"', 'href="/hvac/"'),
    ('href="/commercial-hvac/rooftop/"', 'href="/commercial-hvac/"'),
    ('href="/commercial-hvac/vrf/"', 'href="/commercial-hvac/"'),
    ('href="/commercial-hvac/chillers/"', 'href="/commercial-hvac/"'),
    # Electrical
    ('href="/electrical/panels/"', 'href="/electrical/"'),
    ('href="/electrical/breakers/"', 'href="/electrical/"'),
    ('href="/electrical/surge-protection/"', 'href="/electrical/"'),
    ('href="/electrical/multimeters/"', 'href="/electrical/"'),
    ('href="/electrical/wire-strippers/"', 'href="/electrical/"'),
    ('href="/electrical/conduit/"', 'href="/electrical/"'),
    # Pumps
    ('href="/pumps/centrifugal/"', 'href="/pumps/"'),
    ('href="/pumps/circulator/"', 'href="/pumps/"'),
    ('href="/pumps/booster/"', 'href="/pumps/"'),
    ('href="/pumps/sump/"', 'href="/pumps/"'),
    ('href="/pumps/sewage/"', 'href="/pumps/"'),
    ('href="/pumps/utility/"', 'href="/pumps/"'),
    # More
    ('href="/air-quality/air-purifiers/"', 'href="/air-quality/"'),
    ('href="/air-quality/dehumidifiers/"', 'href="/air-quality/"'),
    ('href="/air-quality/ventilation/"', 'href="/air-quality/"'),
    ('href="/air-quality/filters/"', 'href="/air-quality/"'),
    ('href="/water-heating/heat-pump-wh/"', 'href="/water-heating/"'),
    ('href="/water-heating/tankless/"', 'href="/water-heating/"'),
    ('href="/water-heating/solar/"', 'href="/water-heating/"'),
]

count = 0
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        count += 1

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Tamamlandi! {count} link guncellendi.")
