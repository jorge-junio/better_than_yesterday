(() => {
  'use strict';
  function renderDistribution(target, sourceId) {
    const sourceElement = document.getElementById(sourceId);
    if (!target || !sourceElement) return;
    const source = JSON.parse(sourceElement.textContent);
    const total = source.values.reduce((sum, value) => sum + value, 0);
    const colors = ['var(--success)', 'var(--warning)', 'var(--danger)'];
    const track = document.createElement('div');
    track.className = 'distribution-track';
    const legend = document.createElement('div');
    legend.className = 'distribution-legend';
    source.values.forEach((value, index) => {
      const segment = document.createElement('span');
      segment.className = 'distribution-segment';
      segment.style.width = `${total ? value / total * 100 : 0}%`;
      segment.style.backgroundColor = colors[index];
      track.append(segment);
      const row = document.createElement('p');
      const dot = document.createElement('span');
      dot.className = 'legend-dot';
      dot.style.backgroundColor = colors[index];
      row.append(dot, document.createTextNode(`${source.labels[index]}: ${value}`));
      legend.append(row);
    });
    if (!total) {
      const empty = document.createElement('p');
      empty.textContent = 'Nenhuma tarefa neste intervalo.';
      legend.append(empty);
    }
    target.replaceChildren(track, legend);
  }
  renderDistribution(document.querySelector('[data-chart="today"]'), 'completion-chart-data');
  renderDistribution(document.querySelector('[data-chart="range"]'), 'range-status-chart-data');

  if (new URLSearchParams(location.search).get('completed') === '1') {
    const avatar = document.querySelector('[data-avatar]');
    if (avatar) avatar.dataset.state = 'celebrating';
    avatar?.addEventListener('animationend', () => { avatar.dataset.state = 'idle'; }, { once: true });
    window.BTY.toast('Missão concluída. Mais um passo na sua jornada!');
    const url = new URL(location.href);
    url.searchParams.delete('completed');
    history.replaceState(null, '', url);
  }
  document.querySelectorAll('[data-complete-quest]').forEach((form) => {
    form.addEventListener('submit', () => {
      const button = form.querySelector('button');
      button.disabled = true;
      button.setAttribute('aria-label', 'Concluindo missão');
    });
  });
  // Refresh real data in the background without interrupting a form or dialog.
  let filterDirty = false;
  document.querySelector('.date-filters')?.addEventListener('input', () => { filterDirty = true; });
  setInterval(async () => {
    if (location.pathname !== '/dashboard/' || document.hidden || document.querySelector('dialog[open]') || filterDirty || document.activeElement?.closest('form')) return;
    try {
      const response = await fetch(location.href, { credentials: 'same-origin' });
      if (!response.ok || response.redirected) return;
      const next = new DOMParser().parseFromString(await response.text(), 'text/html');
      const content = next.getElementById('page-content');
      // Full reload preserves native form behavior and keeps the URL's filters.
      if (content && content.textContent !== document.getElementById('page-content').textContent) {
        const scrollPosition = window.scrollY;
        sessionStorage.setItem('bty-dashboard-scroll', String(scrollPosition));
        location.reload();
      }
    } catch { /* A connection failure leaves the current data and controls intact. */ }
  }, 60000);
  const savedScroll = sessionStorage.getItem('bty-dashboard-scroll');
  if (savedScroll !== null) {
    sessionStorage.removeItem('bty-dashboard-scroll');
    window.scrollTo({ top: Number(savedScroll), behavior: 'instant' });
  }
})();
