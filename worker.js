export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const response = await env.ASSETS.fetch(request);
    
    // Fix content-type for sitemap and robots
    if (url.pathname === '/sitemap.xml') {
      return new Response(response.body, {
        headers: {
          'Content-Type': 'application/xml',
          'Cache-Control': 'public, max-age=3600',
        }
      });
    }
    if (url.pathname === '/robots.txt') {
      return new Response(response.body, {
        headers: { 'Content-Type': 'text/plain' }
      });
    }
    return response;
  }
};
