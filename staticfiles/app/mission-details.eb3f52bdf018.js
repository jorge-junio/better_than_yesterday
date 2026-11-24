(() => {
  const dialog = document.querySelector('[data-mission-details-dialog]');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const content = dialog.querySelector('[data-mission-details-content]');
  let controller;
  let opener;
  const close = () => dialog.close();
  dialog.querySelector('[data-close-mission-details]').addEventListener('click', close);
  let outsidePress = false;
  const outside = (event) => {
    const rect = dialog.getBoundingClientRect();
    return event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom);
  };
  dialog.addEventListener('pointerdown', (event) => { outsidePress = outside(event); });
  dialog.addEventListener('click', (event) => {
    if (outsidePress && outside(event)) close();
    outsidePress = false;
  });
  dialog.addEventListener('close', () => {
    controller?.abort();
    content.replaceChildren();
    document.body.classList.remove('mission-details-open');
    opener?.focus({ preventScroll: true });
  });
  document.addEventListener('click', async (event) => {
    const link = event.target.closest('[data-mission-details]');
    if (!link || event.defaultPrevented || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    opener = link;
    controller?.abort();
    const request = new AbortController();
    controller = request;
    content.textContent = 'Carregando detalhes…';
    dialog.showModal();
    document.body.classList.add('mission-details-open');
    try {
      const url = new URL(link.href);
      url.searchParams.set('dialog', '1');
      url.searchParams.set('back', location.pathname + location.search);
      const response = await fetch(url, { credentials: 'same-origin', headers: { 'HX-Request': 'true' }, signal: request.signal });
      if (!response.ok || response.redirected) throw new Error('Could not load details');
      const doc = new DOMParser().parseFromString(await response.text(), 'text/html');
      const details = doc.querySelector('.task-detail');
      if (!details) throw new Error('Missing details');
      if (request.signal.aborted || !dialog.open) return;
      content.replaceChildren(details);
    } catch (error) {
      if (request.signal.aborted) return;
      const message = document.createElement('p');
      message.textContent = 'Não foi possível carregar os detalhes. Tente novamente ou abra a página da missão.';
      const fallback = document.createElement('a');
      fallback.href = link.href;
      fallback.className = 'btn';
      fallback.textContent = 'Abrir detalhes';
      content.replaceChildren(message, fallback);
    }
  });
})();
