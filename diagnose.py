import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Referer': 'https://www.google.com/',
}

url = 'https://hvacdirect.com/air-conditioner-condensers.html'
r = requests.get(url, headers=HEADERS, timeout=15)
print("STATUS:", r.status_code)
print("LENGTH:", len(r.text))
print("FIRST 1500 CHARS:")
print(r.text[:1500])
print("\n\n--- does it contain 'product-item'? ---")
print('product-item' in r.text)
print("--- does it contain 'captcha' or 'blocked' or 'Access Denied'? ---")
for kw in ['captcha', 'Access Denied', 'blocked', 'cf-browser-verification', 'Just a moment']:
    if kw.lower() in r.text.lower():
        print(f"FOUND: {kw}")
