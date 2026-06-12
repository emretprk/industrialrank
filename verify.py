import re, requests, random
from pathlib import Path

pub = Path('public')
headers = {'User-Agent': 'Mozilla/5.0'}
files = [f for f in pub.rglob('index.html') if len(f.parts) >= 3]
sample = random.sample(files, 20)

ok = bad = 0
for f in sample:
    html = f.read_text(errors='ignore')
    urls = re.findall(r'href="(https://hvacdirect\.com/[^"]+\.html[^"]*)"', html)
    if not urls:
        print(f"NO URL: {f.parent}")
        bad += 1
        continue
    url = urls[0].split('?')[0]
    r = requests.head(url, headers=headers, timeout=5)
    status = "OK" if r.status_code == 200 else f"FAIL({r.status_code})"
    print(f"{status}: {f.parent.name[:50]}")
    if r.status_code == 200: ok += 1
    else: bad += 1

print(f"\nSonuc: {ok} OK, {bad} FAIL")
