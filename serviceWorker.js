// 受け取ったらキャッシュではなく自動保存に向けて download トリガー
self.addEventListener('fetch', (event) => {
  if (event.request.url.includes('/run')) {
    event.respondWith(
      fetch(event.request).then(response =>
        response.blob().then(blob => {
          const url = URL.createObjectURL(blob);
          const a = new Response(blob).headers.get("Content-Type").includes("text") ?
            'result.pokemogukunnstxt' : 'result.pokemogukunnsbin';

          const anchor = self.document.createElement('a');
          anchor.href = url;
          anchor.download = a;
          anchor.click();
          return response;
        })
      )
    );
  }
});
