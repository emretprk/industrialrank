#!/usr/bin/env python3
"""
IndustrialRank Nav Düzeltici
Dropdown'lardaki spesifik ürün linklerini kaldırır,
sadece kategori linkleri bırakır.
"""

NEW_NAV = '''<nav>
  <div class="nav-links">

    <div class="has-dropdown">
      <a href="/heat-pumps/">Heat Pumps</a>
      <div class="dropdown">
        <div class="dropdown-col">
          <div class="dropdown-col-title">By Type</div>
          <a href="/heat-pumps/air-source/"><strong>Air Source</strong><span>Most common · DIY friendly</span></a>
          <a href="/heat-pumps/ground-source/"><strong>Ground Source</strong><span>Highest efficiency</span></a>
          <a href="/heat-pumps/mini-split/"><strong>Mini Split</strong><span>Ductless · Zone control</span></a>
          <a href="/heat-pumps/dual-fuel/"><strong>Dual Fuel</strong><span>Hybrid gas + heat pump</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">By Brand</div>
          <a href="/brands/mitsubishi/"><strong>Mitsubishi</strong><span>Hyper-Heat · Cold climate</span></a>
          <a href="/brands/daikin/"><strong>Daikin</strong><span>VRV · Commercial grade</span></a>
          <a href="/brands/carrier/"><strong>Carrier</strong><span>Infinity series</span></a>
          <a href="/brands/goodman/"><strong>Goodman</strong><span>Best value</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Resources</div>
          <a href="/heat-pumps/">All Heat Pump Reviews →</a>
          <a href="/guides/">Buying Guides</a>
          <a href="/compare/">Compare Models</a>
        </div>
      </div>
    </div>

    <div class="has-dropdown">
      <a href="/mini-splits/">Mini Splits</a>
      <div class="dropdown">
        <div class="dropdown-col">
          <div class="dropdown-col-title">DIY Systems</div>
          <a href="/mini-splits/diy/"><strong>DIY Mini Splits</strong><span>No technician required</span></a>
          <a href="/mini-splits/single-zone/"><strong>Single Zone</strong><span>One room · One unit</span></a>
          <a href="/mini-splits/multi-zone/"><strong>Multi Zone</strong><span>Multiple rooms</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">By BTU</div>
          <a href="/mini-splits/9000-btu/"><strong>9,000 BTU</strong><span>Up to 350 sq ft</span></a>
          <a href="/mini-splits/12000-btu/"><strong>12,000 BTU</strong><span>Up to 550 sq ft</span></a>
          <a href="/mini-splits/18000-btu/"><strong>18,000 BTU</strong><span>Up to 850 sq ft</span></a>
          <a href="/mini-splits/24000-btu/"><strong>24,000 BTU</strong><span>Up to 1,500 sq ft</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Resources</div>
          <a href="/mini-splits/">All Mini Split Reviews →</a>
          <a href="/guides/">Installation Guides</a>
          <a href="/compare/">Compare Models</a>
        </div>
      </div>
    </div>

    <div class="has-dropdown">
      <a href="/hvac/">Air Conditioners</a>
      <div class="dropdown">
        <div class="dropdown-col">
          <div class="dropdown-col-title">Central AC</div>
          <a href="/hvac/central-air/"><strong>Central Air</strong><span>Whole home cooling</span></a>
          <a href="/hvac/window-units/"><strong>Window Units</strong><span>Single room</span></a>
          <a href="/hvac/portable/"><strong>Portable AC</strong><span>No installation needed</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Commercial</div>
          <a href="/commercial-hvac/"><strong>Commercial HVAC</strong><span>5+ ton systems</span></a>
          <a href="/commercial-hvac/rooftop/"><strong>Rooftop Units</strong><span>RTU · BACnet ready</span></a>
          <a href="/commercial-hvac/vrf/"><strong>VRF Systems</strong><span>Variable refrigerant flow</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Resources</div>
          <a href="/hvac/">All AC Reviews →</a>
          <a href="/guides/">Sizing Guides</a>
        </div>
      </div>
    </div>

    <div class="has-dropdown">
      <a href="/electrical/">Electrical</a>
      <div class="dropdown">
        <div class="dropdown-col">
          <div class="dropdown-col-title">Panels &amp; Breakers</div>
          <a href="/electrical/panels/"><strong>Load Centers</strong><span>Main panels · Sub panels</span></a>
          <a href="/electrical/breakers/"><strong>Circuit Breakers</strong><span>AFCI · GFCI · Standard</span></a>
          <a href="/electrical/surge-protection/"><strong>Surge Protection</strong><span>Whole home protection</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Tools &amp; Meters</div>
          <a href="/electrical/multimeters/"><strong>Multimeters</strong><span>Digital · Clamp meters</span></a>
          <a href="/electrical/wire-strippers/"><strong>Wire Strippers</strong><span>Manual · Auto-strip</span></a>
          <a href="/electrical/conduit/"><strong>Conduit &amp; Fittings</strong><span>EMT · PVC · Rigid</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Resources</div>
          <a href="/electrical/">All Electrical Reviews →</a>
          <a href="/guides/">Wiring Guides</a>
        </div>
      </div>
    </div>

    <div class="has-dropdown">
      <a href="/pumps/">Pumps</a>
      <div class="dropdown">
        <div class="dropdown-col">
          <div class="dropdown-col-title">Process &amp; Industrial</div>
          <a href="/pumps/centrifugal/"><strong>Centrifugal Pumps</strong><span>High flow · ANSI B73.1</span></a>
          <a href="/pumps/circulator/"><strong>Circulator Pumps</strong><span>Hydronic · DHW systems</span></a>
          <a href="/pumps/booster/"><strong>Booster Pumps</strong><span>Pressure boosting</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Sump &amp; Drainage</div>
          <a href="/pumps/sump/"><strong>Sump Pumps</strong><span>Submersible · Pedestal</span></a>
          <a href="/pumps/sewage/"><strong>Sewage Pumps</strong><span>Effluent · Grinder</span></a>
          <a href="/pumps/utility/"><strong>Utility Pumps</strong><span>Transfer · Dewatering</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Resources</div>
          <a href="/pumps/">All Pump Reviews →</a>
          <a href="/guides/">Selection Guides</a>
        </div>
      </div>
    </div>

    <div class="has-dropdown">
      <a href="/air-quality/">More</a>
      <div class="dropdown">
        <div class="dropdown-col">
          <div class="dropdown-col-title">Air Quality</div>
          <a href="/air-quality/air-purifiers/"><strong>Air Purifiers</strong><span>HEPA · UV · Ionizer</span></a>
          <a href="/air-quality/dehumidifiers/"><strong>Dehumidifiers</strong><span>Whole home · Portable</span></a>
          <a href="/air-quality/ventilation/"><strong>Ventilation (ERV)</strong><span>Energy recovery</span></a>
          <a href="/air-quality/filters/"><strong>Air Filters</strong><span>MERV ratings · HEPA</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Water Heating</div>
          <a href="/water-heating/heat-pump-wh/"><strong>Heat Pump WH</strong><span>3-4x more efficient</span></a>
          <a href="/water-heating/tankless/"><strong>Tankless</strong><span>On-demand · Gas · Electric</span></a>
          <a href="/water-heating/solar/"><strong>Solar WH</strong><span>IRA tax credit eligible</span></a>
        </div>
        <div class="dropdown-col">
          <div class="dropdown-col-title">Commercial HVAC</div>
          <a href="/commercial-hvac/"><strong>Commercial HVAC</strong><span>5-ton+ systems</span></a>
          <a href="/commercial-hvac/vrf/"><strong>VRF Systems</strong><span>Variable refrigerant flow</span></a>
          <a href="/commercial-hvac/chillers/"><strong>Chillers</strong><span>Large building cooling</span></a>
        </div>
      </div>
    </div>

  </div>
  <a href="/find/" class="nav-btn">Find Equipment</a>
  <button class="hamburger" onclick="toggleMenu(this)" aria-label="Menu"><span></span><span></span><span></span><span></span></button>
</nav>'''

import re

filepath = '/Users/emretoprak/Downloads/industrialrank/public/index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# <nav> ... </nav> bloğunu bul ve değiştir
new_content = re.sub(r'<nav>.*?</nav>', NEW_NAV, content, flags=re.DOTALL)

if new_content == content:
    print("HATA: Nav bloğu bulunamadı!")
else:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Nav başarıyla güncellendi!")
