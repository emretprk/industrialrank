// Cloudflare Pages Function: /img?u=<encoded hvacdirect.com image url>
// Proxies HVACDirect product images through our own domain, sending a
// same-site Referer so HVACDirect's hotlink protection doesn't block it.

export async function onRequestGet(context) {
  const url = new URL(context.request.url);
  const imgUrl = url.searchParams.get('u');

  if (!imgUrl || !imgUrl.startsWith('https://hvacdirect.com/')) {
    return new Response('Bad Request', { status: 400 });
  }

  try {
    const imgResponse = await fetch(imgUrl, {
      cf: { cacheEverything: true, cacheTtl: 2592000 },
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://hvacdirect.com/',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
      },
    });

    if (imgResponse.ok) {
      const contentType = imgResponse.headers.get('Content-Type') || 'image/jpeg';
      return new Response(imgResponse.body, {
        headers: {
          'Content-Type': contentType,
          'Cache-Control': 'public, max-age=2592000',
          'Access-Control-Allow-Origin': '*',
        },
      });
    }

    return new Response('Image not found', { status: 404 });
  } catch (e) {
    return new Response('Proxy error', { status: 502 });
  }
}
