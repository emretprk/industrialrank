#!/usr/bin/env python3
"""
IndustrialRank Search Modal Ekleyici
Nav'a search butonu ekler, tıklayınca modal açılır.
Desktop ve mobile uyumlu.
"""

import re

FILEPATH = '/Users/emretoprak/Downloads/industrialrank/public/index.html'

# Search butonu - nav-btn'den önce eklenecek
SEARCH_BTN = '<button class="search-trigger" onclick="openSearch()" aria-label="Search"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg></button>'

# Search modal HTML + CSS + JS
SEARCH_MODAL = '''
<!-- SEARCH MODAL -->
<div id="searchModal" class="search-modal" onclick="if(event.target===this)closeSearch()">
  <div class="search-box">
    <div class="search-header">
      <div class="search-input-wrap">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
        <input type="text" id="searchInput" placeholder="Search equipment, brands, BTU..." autocomplete="off" oninput="handleSearch(this.value)">
        <button class="search-clear" id="searchClear" onclick="clearSearch()" style="display:none">✕</button>
      </div>
      <button class="search-close" onclick="closeSearch()">✕</button>
    </div>
    <div class="search-filters" id="searchFilters">
      <button class="sf-btn active" onclick="setFilter('all',this)">All</button>
      <button class="sf-btn" onclick="setFilter('mini-splits',this)">Mini Splits</button>
      <button class="sf-btn" onclick="setFilter('heat-pumps',this)">Heat Pumps</button>
      <button class="sf-btn" onclick="setFilter('air-conditioners',this)">AC</button>
      <button class="sf-btn" onclick="setFilter('electrical',this)">Electrical</button>
      <button class="sf-btn" onclick="setFilter('pumps',this)">Pumps</button>
    </div>
    <div class="search-results" id="searchResults">
      <div class="search-empty" id="searchEmpty">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.3"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
        <p>Search 9,000+ industrial equipment reviews</p>
      </div>
    </div>
  </div>
</div>

<style>
.search-trigger{background:none;border:none;color:rgba(255,255,255,0.7);cursor:pointer;padding:8px;display:flex;align-items:center;transition:color .15s;margin-right:4px}
.search-trigger:hover{color:#fff}
.search-modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.7);z-index:999;backdrop-filter:blur(4px);padding:16px}
.search-modal.open{display:flex;align-items:flex-start;justify-content:center;padding-top:80px}
.search-box{background:#fff;border-radius:12px;width:100%;max-width:680px;box-shadow:0 24px 64px rgba(0,0,0,0.3);overflow:hidden}
.search-header{display:flex;align-items:center;gap:8px;padding:16px;border-bottom:1px solid #e5e7eb}
.search-input-wrap{flex:1;display:flex;align-items:center;gap:10px;background:#f9fafb;border:1.5px solid #e5e7eb;border-radius:8px;padding:10px 14px;transition:border-color .15s}
.search-input-wrap:focus-within{border-color:#FF5C1A}
.search-input-wrap svg{color:#9ca3af;flex-shrink:0}
.search-input-wrap input{flex:1;border:none;background:none;outline:none;font-size:16px;color:#111;font-family:inherit}
.search-input-wrap input::placeholder{color:#9ca3af}
.search-clear{background:none;border:none;color:#9ca3af;cursor:pointer;font-size:14px;padding:0;line-height:1}
.search-close{background:none;border:none;color:#6b7280;cursor:pointer;font-size:20px;padding:4px 8px;line-height:1;flex-shrink:0}
.search-close:hover{color:#111}
.search-filters{display:flex;gap:6px;padding:12px 16px;border-bottom:1px solid #f3f4f6;overflow-x:auto;scrollbar-width:none}
.search-filters::-webkit-scrollbar{display:none}
.sf-btn{background:none;border:1.5px solid #e5e7eb;border-radius:20px;padding:5px 14px;font-size:12px;font-weight:600;color:#6b7280;cursor:pointer;white-space:nowrap;transition:all .15s;font-family:inherit;letter-spacing:.03em}
.sf-btn:hover{border-color:#FF5C1A;color:#FF5C1A}
.sf-btn.active{background:#FF5C1A;border-color:#FF5C1A;color:#fff}
.search-results{max-height:480px;overflow-y:auto;padding:8px 0}
.search-empty{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:48px 24px;gap:12px;color:#9ca3af;text-align:center}
.search-empty p{font-size:14px;margin:0}
.search-result-item{display:flex;align-items:center;gap:12px;padding:10px 16px;cursor:pointer;transition:background .1s;text-decoration:none;color:inherit}
.search-result-item:hover{background:#f9fafb}
.sri-img{width:52px;height:52px;object-fit:contain;border-radius:6px;background:#f3f4f6;flex-shrink:0}
.sri-img-placeholder{width:52px;height:52px;border-radius:6px;background:#f3f4f6;flex-shrink:0;display:flex;align-items:center;justify-content:center;color:#d1d5db;font-size:20px}
.sri-info{flex:1;min-width:0}
.sri-cat{font-size:10px;font-weight:700;color:#FF5C1A;text-transform:uppercase;letter-spacing:.06em;margin-bottom:2px}
.sri-title{font-size:14px;font-weight:600;color:#111;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sri-brand{font-size:12px;color:#6b7280;margin-top:1px}
.sri-right{text-align:right;flex-shrink:0}
.sri-price{font-size:14px;font-weight:700;color:#111}
.sri-score{font-size:11px;color:#FF5C1A;font-weight:600}
.search-no-results{padding:32px 24px;text-align:center;color:#6b7280;font-size:14px}
.search-result-count{padding:6px 16px;font-size:11px;color:#9ca3af;font-weight:500;letter-spacing:.04em;text-transform:uppercase}
@media(max-width:768px){.search-modal.open{padding-top:16px;align-items:flex-end}.search-box{border-radius:16px 16px 0 0;max-width:100%}.search-results{max-height:60vh}}
</style>

<script>
(function(){
  var idx = null;
  var activeFilter = 'all';
  var searchTimeout = null;

  function loadIndex(cb){
    if(idx){cb(idx);return;}
    fetch('/search-index.json')
      .then(function(r){return r.json();})
      .then(function(data){idx=data;cb(idx);})
      .catch(function(){idx=[];cb([]);});
  }

  window.openSearch = function(){
    document.getElementById('searchModal').classList.add('open');
    document.body.style.overflow='hidden';
    setTimeout(function(){document.getElementById('searchInput').focus();},100);
    loadIndex(function(){});
  };

  window.closeSearch = function(){
    document.getElementById('searchModal').classList.remove('open');
    document.body.style.overflow='';
  };

  window.clearSearch = function(){
    document.getElementById('searchInput').value='';
    document.getElementById('searchClear').style.display='none';
    showEmpty();
  };

  window.setFilter = function(filter, btn){
    activeFilter = filter;
    document.querySelectorAll('.sf-btn').forEach(function(b){b.classList.remove('active');});
    btn.classList.add('active');
    var q = document.getElementById('searchInput').value;
    if(q.length > 1) doSearch(q);
  };

  window.handleSearch = function(q){
    document.getElementById('searchClear').style.display = q ? 'block' : 'none';
    clearTimeout(searchTimeout);
    if(!q || q.length < 2){showEmpty();return;}
    searchTimeout = setTimeout(function(){doSearch(q);}, 150);
  };

  function showEmpty(){
    document.getElementById('searchResults').innerHTML = '<div class="search-empty"><svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.3"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg><p>Search 9,000+ industrial equipment reviews</p></div>';
  }

  function doSearch(q){
    loadIndex(function(data){
      var ql = q.toLowerCase();
      var results = data.filter(function(p){
        if(activeFilter !== 'all' && p.category !== activeFilter) return false;
        return (p.title||'').toLowerCase().indexOf(ql) > -1 ||
               (p.brand||'').toLowerCase().indexOf(ql) > -1 ||
               (p.category||'').toLowerCase().indexOf(ql) > -1;
      }).slice(0, 20);

      var html = '';
      if(results.length === 0){
        html = '<div class="search-no-results">No results for "<strong>'+q+'</strong>"</div>';
      } else {
        html += '<div class="search-result-count">'+results.length+' results</div>';
        results.forEach(function(p){
          var imgHtml = p.image
            ? '<img class="sri-img" src="'+p.image+'" alt="'+p.title+'" loading="lazy" referrerpolicy="no-referrer">'
            : '<div class="sri-img-placeholder">⚙</div>';
          var catLabel = (p.category||'').replace(/-/g,' ').replace(/\b\w/g,function(c){return c.toUpperCase();});
          html += '<a href="'+p.url+'" class="search-result-item" onclick="closeSearch()">'
            + imgHtml
            + '<div class="sri-info">'
            + '<div class="sri-cat">'+catLabel+'</div>'
            + '<div class="sri-title">'+p.title+'</div>'
            + '<div class="sri-brand">'+(p.brand||'')+'</div>'
            + '</div>'
            + '<div class="sri-right">'
            + (p.price ? '<div class="sri-price">'+p.price+'</div>' : '')
            + (p.score ? '<div class="sri-score">★ '+p.score+'</div>' : '')
            + '</div>'
            + '</a>';
        });
      }
      document.getElementById('searchResults').innerHTML = html;
    });
  }

  document.addEventListener('keydown', function(e){
    if(e.key==='Escape') closeSearch();
    if((e.metaKey||e.ctrlKey) && e.key==='k'){e.preventDefault();openSearch();}
  });
})();
</script>
'''

def main():
    with open(FILEPATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Search butonu ekle — nav-btn'den önce
    if 'search-trigger' in content:
        print("Search butonu zaten var, sadece modal güncelleniyor...")
        # Modal varsa güncelle
        content = re.sub(r'<!-- SEARCH MODAL -->.*?</script>', SEARCH_MODAL.strip(), content, flags=re.DOTALL)
    else:
        # Nav-btn'den önce search butonunu ekle
        content = content.replace(
            '<a href="/find/" class="nav-btn">',
            SEARCH_BTN + '\n  <a href="/find/" class="nav-btn">'
        )
        # </nav> öncesine modal ekle
        content = content.replace('</nav>', '</nav>\n' + SEARCH_MODAL)

    with open(FILEPATH, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Search modal basariyla eklendi!")
    print("Test: industrialrank.com aç, nav'daki 🔍 butonuna tıkla")

if __name__ == '__main__':
    main()
