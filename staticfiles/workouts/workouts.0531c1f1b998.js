(() => {
  const charts = [];
  const setStatus = (form, message, failed = false) => {
    const status = form && form.querySelector('[data-save-status]');
    if (!status) return;
    status.textContent = message;
    status.classList.toggle('text-danger', failed);
    status.classList.remove('text-success');
  };
  const dirtyForms = () => [...document.querySelectorAll('[data-set-form][data-dirty="true"]')];
  document.addEventListener('input', (event) => {
    const form = event.target.closest('[data-set-form]');
    if (!form) return;
    form.dataset.dirty = 'true';
    setStatus(form, 'Alteração ainda não salva');
  });
  document.addEventListener('htmx:beforeRequest', (event) => {
    const form = event.detail.elt.closest('[data-set-form]');
    if (!form) return;
    form.setAttribute('aria-busy', 'true');
    setStatus(form, 'Salvando…');
  });
  document.addEventListener('htmx:afterRequest', (event) => {
    const form = event.detail.elt.closest('[data-set-form]');
    if (!form) return;
    form.removeAttribute('aria-busy');
    if (!event.detail.successful) {
      form.dataset.dirty = 'true';
      setStatus(form, 'Falha ao salvar. Verifique a conexão e tente novamente.', true);
    }
  });
  document.addEventListener('htmx:confirm', (event) => {
    const form = event.detail.elt.closest('[data-set-form]');
    if (form || !dirtyForms().length) return;
    event.preventDefault();
    if (window.confirm('Há séries com alterações ainda não salvas. Deseja sair sem registrar essas alterações?')) {
      dirtyForms().forEach((item) => delete item.dataset.dirty);
      event.detail.issueRequest(true);
    }
  });
  window.addEventListener('beforeunload', (event) => {
    if (!dirtyForms().length) return;
    event.preventDefault();
    event.returnValue = '';
  });
  let restState = null;
  let restInterval = null;
  const restKey = (sessionId) => `bty-workout-rest-${sessionId}`;
  const storeRestState = () => {
    if (!restState) return;
    try { sessionStorage.setItem(restKey(restState.sessionId), JSON.stringify(restState)); } catch (_) { /* The current page still keeps the countdown. */ }
  };
  const loadRestState = (sessionId) => {
    try {
      const state = JSON.parse(sessionStorage.getItem(restKey(sessionId)));
      if (state && String(state.sessionId) === sessionId && Number.isFinite(state.deadline) && Number.isInteger(state.seconds) && state.seconds > 0 && state.seconds <= 3600) return state;
    } catch (_) { /* Storage can be unavailable in restricted browser modes. */ }
    return restState && String(restState.sessionId) === sessionId ? restState : null;
  };
  const renderRestTimer = () => {
    const timer = document.querySelector('[data-rest-timer]');
    if (!timer || !restState || String(restState.sessionId) !== timer.dataset.sessionId) return;
    const remaining = Math.max(0, Math.ceil((restState.deadline - Date.now()) / 1000));
    timer.hidden = false;
    timer.closest('.workout-page').classList.add('rest-timer-visible');
    timer.querySelector('[data-rest-time]').textContent = `${String(Math.floor(remaining / 60)).padStart(2, '0')}:${String(remaining % 60).padStart(2, '0')}`;
    const percentage = Math.min(100, Math.round(remaining / restState.seconds * 100));
    const progress = timer.querySelector('[data-rest-progress]');
    progress.style.width = `${percentage}%`;
    progress.setAttribute('aria-valuenow', String(percentage));
    const status = timer.querySelector('[data-rest-status]');
    const message = remaining ? 'Descansando…' : 'Descanso concluído. Você pode continuar.';
    if (status.textContent !== message) status.textContent = message;
    const button = timer.querySelector('[data-rest-dismiss]');
    button.textContent = remaining ? 'Pular descanso' : 'Fechar';
    button.title = remaining ? 'Pular descanso' : 'Fechar contador';
    if (!remaining && restInterval) {
      window.clearInterval(restInterval);
      restInterval = null;
    }
  };
  const initializeRestTimer = () => {
    if (restInterval) window.clearInterval(restInterval);
    restInterval = null;
    const timer = document.querySelector('[data-rest-timer]');
    if (!timer) return;
    restState = loadRestState(timer.dataset.sessionId);
    if (!restState) return;
    restInterval = window.setInterval(renderRestTimer, 250);
    renderRestTimer();
  };
  document.addEventListener('workoutRestStarted', (event) => {
    const timer = document.querySelector('[data-rest-timer]');
    const seconds = Number(event.detail.seconds);
    if (!timer || String(event.detail.sessionId) !== timer.dataset.sessionId || !Number.isInteger(seconds) || seconds <= 0 || seconds > 3600) return;
    restState = { sessionId: timer.dataset.sessionId, seconds, deadline: Date.now() + seconds * 1000 };
    storeRestState();
    initializeRestTimer();
  });
  document.addEventListener('click', (event) => {
    const button = event.target.closest('[data-rest-dismiss]');
    if (!button) return;
    const timer = button.closest('[data-rest-timer]');
    try { sessionStorage.removeItem(restKey(timer.dataset.sessionId)); } catch (_) { /* Dismiss also works without storage. */ }
    restState = null;
    if (restInterval) window.clearInterval(restInterval);
    restInterval = null;
    timer.hidden = true;
    timer.closest('.workout-page').classList.remove('rest-timer-visible');
  });
  document.addEventListener('visibilitychange', renderRestTimer);
  document.addEventListener('DOMContentLoaded', initializeRestTimer);
  document.addEventListener('htmx:afterSwap', (event) => {
    if (event.detail.target.id === 'page-content') initializeRestTimer();
  });
  const renderCharts = () => {
    charts.splice(0).forEach((chart) => chart.destroy());
    const source = document.getElementById('workout-evolution-data');
    if (!source || !window.Chart) return;
    const data = JSON.parse(source.textContent);
    [['workout-weight-chart', 'Maior carga (kg)', data.weights, '#14b8a6'], ['workout-repetitions-chart', 'Repetições totais', data.repetitions, '#60a5fa']].forEach(([id, label, values, color]) => {
      const canvas = document.getElementById(id);
      if (!canvas) return;
      charts.push(new Chart(canvas, {
        type: 'line', data: { labels: data.labels, datasets: [{ label, data: values, borderColor: color, backgroundColor: color, tension: .2 }] },
        options: { responsive: true, maintainAspectRatio: false, scales: { x: { ticks: { color: '#cbd5e1' }, grid: { color: 'rgba(255,255,255,.08)' } }, y: { beginAtZero: true, ticks: { color: '#cbd5e1' }, grid: { color: 'rgba(255,255,255,.08)' } } }, plugins: { legend: { labels: { color: '#cbd5e1' } } } },
      }));
    });
  };
  document.addEventListener('DOMContentLoaded', renderCharts);
  document.addEventListener('htmx:afterSwap', (event) => {
    if (event.detail.target.id === 'page-content') renderCharts();
  });
})();
