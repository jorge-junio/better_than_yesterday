(() => {
  const updateTrainingDay = () => {
    document.querySelectorAll('[data-training-day-picker]').forEach((picker) => {
      const select = picker.querySelector('select[name="weekday"]');
      if (!select) return;
      picker.querySelectorAll('[data-training-day]').forEach((day) => {
        day.hidden = day.dataset.trainingDay !== select.value;
      });
    });
  };
  document.addEventListener('change', (event) => {
    if (event.target.matches('[data-training-day-picker] select[name="weekday"]')) updateTrainingDay();
  });
  document.addEventListener('DOMContentLoaded', updateTrainingDay);
  document.addEventListener('app:ready', updateTrainingDay);
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
  document.addEventListener('app:save-started', (event) => {
    const form = event.detail.form;
    if (form.matches('[data-set-form]')) setStatus(form, 'Salvando…');
  });
  document.addEventListener('app:save-failed', (event) => {
    const form = event.detail.form;
    if (form.matches('[data-set-form]')) {
      form.dataset.dirty = 'true';
      setStatus(form, 'Falha ao salvar. Verifique a conexão e tente novamente.', true);
    }
  });
  document.addEventListener('click', (event) => {
    const link = event.target.closest('a[href]');
    if (!link || link.getAttribute('href').startsWith('#') || !dirtyForms().length) return;
    if (!window.confirm('Há séries com alterações ainda não salvas. Deseja sair sem registrar essas alterações?')) {
      event.preventDefault(); event.stopImmediatePropagation();
    } else dirtyForms().forEach((form) => delete form.dataset.dirty);
  }, true);
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
  document.addEventListener('app:ready', initializeRestTimer);
  const renderCharts = () => {
    const source = document.getElementById('workout-evolution-data');
    if (!source) return;
    const data = JSON.parse(source.textContent);
    const ns = 'http://www.w3.org/2000/svg';
    const element = (name, attrs = {}) => { const node = document.createElementNS(ns, name); Object.entries(attrs).forEach(([key, value]) => node.setAttribute(key, value)); return node; };
    [['workout-weight-chart', 'Maior carga (kg)', data.weights], ['workout-repetitions-chart', 'Repetições totais', data.repetitions]].forEach(([id, label, values]) => {
      const target = document.getElementById(id);
      if (!target) return;
      const svg = element('svg', { viewBox: '0 0 440 220', role: 'img', 'aria-label': label, class: 'svg-chart' });
      const max = Math.max(1, ...values.map(Number));
      const points = values.map((value, index) => [40 + index / Math.max(values.length - 1, 1) * 380, 180 - Number(value) / max * 150]);
      for (let n = 0; n <= 3; n++) {
        const y = 180 - n * 50;
        svg.append(element('line', { x1: 40, y1: y, x2: 420, y2: y, class: 'chart-grid' }));
        const text = element('text', { x: 3, y: y + 4 }); text.textContent = String(Math.round(max * n / 3 * 10) / 10); svg.append(text);
      }
      svg.append(element('polyline', { points: points.map(p => p.join(',')).join(' '), fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }));
      points.forEach(([x, y], index) => { const dot = element('circle', { cx:x, cy:y, r:4, fill:'currentColor' }); const title = element('title'); title.textContent = `${data.labels[index]}: ${values[index]}`; dot.append(title); svg.append(dot); });
      if (data.labels.length) { for (const [x, index] of [[40,0],[420,data.labels.length - 1]]) { const text = element('text', {x, y:205, 'text-anchor': x === 40 ? 'start' : 'end'}); text.textContent = data.labels[index]; svg.append(text); } }
      const caption = document.createElement('p'); caption.className='chart-caption'; caption.textContent=label;
      target.replaceChildren(caption, svg);
    });
  };
  document.addEventListener('DOMContentLoaded', renderCharts);
})();
