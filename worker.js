const SITEMAP = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://industrialrank.com/</loc><lastmod>2026-05-27</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>
  <url><loc>https://industrialrank.com/hvac/</loc><lastmod>2026-05-27</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>
  <url><loc>https://industrialrank.com/electrical/</loc><lastmod>2026-05-27</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>
  <url><loc>https://industrialrank.com/pumps/</loc><lastmod>2026-05-27</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>
  <url><loc>https://industrialrank.com/compare/</loc><lastmod>2026-05-27</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://industrialrank.com/top10/</loc><lastmod>2026-05-27</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://industrialrank.com/find/</loc><lastmod>2026-05-27</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
  <url><loc>https://industrialrank.com/hvac/carrier-infinity-20-heat-pump-review</loc><lastmod>2026-05-27</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>
  <url><loc>https://industrialrank.com/hvac/lennox-xc21-review</loc><lastmod>2026-05-27</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>
  <url><loc>https://industrialrank.com/hvac/daikin-vrv5-review</loc><lastmod>2026-05-27</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>
  <url><loc>https://industrialrank.com/electrical/siemens-q2200-review</loc><lastmod>2026-05-27</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>
  <url><loc>https://industrialrank.com/electrical/eaton-br2020-review</loc><lastmod>2026-05-27</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>
  <url><loc>https://industrialrank.com/electrical/fluke-117-review</loc><lastmod>2026-05-27</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>
  <url><loc>https://industrialrank.com/pumps/grundfos-cm5-5-review</loc><lastmod>2026-05-27</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>
  <url><loc>https://industrialrank.com/pumps/xylem-goulds-3196-review</loc><lastmod>2026-05-27</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>
  <url><loc>https://industrialrank.com/blog/</loc><lastmod>2026-05-27</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>
  <url><loc>https://industrialrank.com/blog/hvac-technologies-2026</loc><lastmod>2026-05-27</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://industrialrank.com/blog/industrial-electrical-trends-2026</loc><lastmod>2026-05-27</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://industrialrank.com/blog/industrial-pump-technology-2026</loc><lastmod>2026-05-27</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://industrialrank.com/blog/industrial-automation-trends-2026</loc><lastmod>2026-05-27</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://industrialrank.com/blog/compressed-air-systems-2026</loc><lastmod>2026-05-27</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://industrialrank.com/about/</loc><lastmod>2026-05-27</lastmod><changefreq>yearly</changefreq><priority>0.5</priority></url>
  <url><loc>https://industrialrank.com/contact/</loc><lastmod>2026-05-27</lastmod><changefreq>yearly</changefreq><priority>0.5</priority></url>
</urlset>`;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === '/sitemap.xml') {
      return new Response(SITEMAP, {
        headers: {
          'Content-Type': 'application/xml; charset=utf-8',
          'Cache-Control': 'public, max-age=3600',
        }
      });
    }

    return env.ASSETS.fetch(request);
  }
};
