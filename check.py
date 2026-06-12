import random
from pathlib import Path
pub = Path('public')
files = [f for f in pub.rglob('index.html') if len(f.parts) >= 3]
for f in random.sample(files, 10):
    html = f.read_text(errors='ignore')
    img = 'product-hero-img' in html
    aff = 'hvacdirect.com' in html
    print(f"{f.parent}: img={img} aff={aff}")
