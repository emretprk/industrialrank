export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // www → non-www 301 redirect
    if (url.hostname === 'www.industrialrank.com') {
      const newUrl = request.url.replace('www.industrialrank.com', 'industrialrank.com');
      return Response.redirect(newUrl, 301);
    }


    // 301 Redirects — old /hvac/ paths
    const redirectMap = {
      "/hvac/carrier-infinity-20-heat-pump-review/": "/heat-pumps/carrier-infinity-20-heat-pump-review/",
      "/hvac/trane-xr15-heat-pump-review/": "/heat-pumps/trane-xr15-heat-pump-review/",
      "/hvac/goodman-gsx160481-heat-pump-review/": "/heat-pumps/goodman-gsx160481-heat-pump-review/",
      "/hvac/bosch-bova-60hdn1-heat-pump-review/": "/heat-pumps/bosch-bova-60hdn1-heat-pump-review/",
      "/hvac/lennox-xp21-heat-pump-review/": "/heat-pumps/lennox-xp21-heat-pump-review/",
      "/hvac/aciq-2ton-18seer2-heat-pump-review/": "/heat-pumps/aciq-2ton-18seer2-heat-pump-review/",
      "/hvac/trane-runtru-2ton-heat-pump-review/": "/heat-pumps/trane-runtru-2ton-heat-pump-review/",
      "/hvac/rheem-rp1648aj1na-heat-pump-review/": "/heat-pumps/rheem-rp1648aj1na-heat-pump-review/",
      "/hvac/lennox-xc21-air-conditioner-review/": "/air-conditioners/lennox-xc21-air-conditioner-review/",
      "/hvac/goodman-gsxh503610-ac-system-review/": "/air-conditioners/goodman-gsxh503610-ac-system-review/",
      "/hvac/carrier-performance-14-ac-review/": "/air-conditioners/carrier-performance-14-ac-review/",
      "/hvac/daikin-vrv5-review/": "/mini-splits/daikin-vrv5-review/",
      "/hvac/mitsubishi-mxz-4c36na-mini-split-review/": "/mini-splits/mitsubishi-mxz-4c36na-mini-split-review/",
      "/hvac/mrcool-diy-24k-mini-split-review/": "/mini-splits/mrcool-diy-24k-mini-split-review/",
    };
    if (redirectMap[url.pathname] || redirectMap[url.pathname + '/']) {
      const target = redirectMap[url.pathname] || redirectMap[url.pathname + '/'];
      return Response.redirect('https://industrialrank.com' + target, 301);
    }

    // Image Proxy — HVACDirect hotlink bypass
    if (url.pathname === '/img/') {
      const imgUrl = url.searchParams.get('u');
      if (!imgUrl || !imgUrl.startsWith('https://hvacdirect.com/')) {
        return new Response('Bad Request', { status: 400 });
      }
      try {
        const imgResponse = await fetch(imgUrl, {
          cf: { cacheEverything: false },
          headers: {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://hvacdirect.com/',
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Dest': 'image',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-origin',
          }
        });
        if (imgResponse.ok) {
          const contentType = imgResponse.headers.get('Content-Type') || 'image/jpeg';
          return new Response(imgResponse.body, {
            headers: {
              'Content-Type': contentType,
              'Cache-Control': 'public, max-age=2592000',
              'Access-Control-Allow-Origin': '*',
            }
          });
        }
        // Fallback: redirect to HVACDirect directly
        return Response.redirect(imgUrl, 302);
      } catch(e) {
        return Response.redirect(imgUrl, 302);
      }
    }
      });
    }

    return env.ASSETS.fetch(request);
  }
};
