import requests, re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Referer': 'https://www.google.com/',
}

url = 'https://hvacdirect.com/1-5-ton-16-seer-goodman-heat-pump-gsz160181.html'
r = requests.get(url, headers=HEADERS, timeout=15)
print("STATUS:", r.status_code)
html = r.text

for pattern in [r'"reviewCount"\s*:\s*"?(\d+)', r'ratingCount["\s:]+(\d+)', r'(\d+)\s+Review']:
    m = re.search(pattern, html)
    print(f"pattern {pattern!r} -> {m.group(1) if m else 'NOT FOUND'}")
