(() => {
  'use strict';
  window.BTY = window.BTY || {};
  const sheet = document.getElementById('mission-sheet');
  let sheetOpener;
  let requestPending = false;
  function toast(message) {
    const target = document.querySelector('[data-app-toast]');
    if (!target) return;
    target.textContent = message; target.hidden = false;
    clearTimeout(target.timer); target.timer = setTimeout(() => { target.hidden = true; }, 4500);
  }
  window.BTY.toast = toast;
  function initialize(root = document) {
    root.querySelectorAll('label:not([for])').forEach((label) => {
      const control = label.nextElementSibling;
      if (control?.id && control.matches('input,select,textarea')) label.htmlFor = control.id;
    });
    root.querySelectorAll('input[name="meanings"]').forEach((input, index) => { input.setAttribute('aria-label', `Significado ${index + 1}`); });
    root.querySelectorAll('table').forEach((table) => {
      table.classList.add('mobile-card-table');
      const labels = [...table.querySelectorAll('thead th')].map((th) => th.textContent.trim());
      table.querySelectorAll('tbody tr').forEach((row) => [...row.cells].forEach((cell, index) => {
        if (!cell.dataset.label && !cell.hasAttribute('colspan') && labels[index]) cell.dataset.label = labels[index];
      }));
    });
    root.querySelectorAll('[data-uppercase]').forEach((input) => { input.value = input.value.toUpperCase(); });
    const recurrence = root.querySelector('[name="recurrence_type"]');
    if (recurrence) updateRecurrence(recurrence);
    const meanings = root.querySelector('#meanings-list');
    if (meanings && !meanings.children.length) addMeaning();
    document.dispatchEvent(new CustomEvent('app:ready', { detail: { root } }));
  }
  window.BTY.initialize = initialize;
  function updateRecurrence(input) {
    input.closest('form').querySelectorAll('[data-recurrence-section]').forEach((section) => {
      section.classList.toggle('d-none', section.dataset.recurrenceSection !== input.value);
    });
  }
  function addMeaning() {
    const list = document.getElementById('meanings-list');
    const template = document.getElementById('meaning-row-template');
    if (!list || !template) return;
    list.append(template.content.cloneNode(true));
    list.querySelectorAll('input').forEach((input, index) => input.setAttribute('aria-label', `Significado ${index + 1}`));
  }
  function feedback(form, message) {
    let target = form.querySelector('[data-request-error]');
    if (!target) { target = document.createElement('p'); target.dataset.requestError = ''; target.className = 'alert alert-danger'; target.setAttribute('role', 'alert'); form.prepend(target); }
    target.textContent = message;
  }
  document.addEventListener('input', (event) => {
    const input = event.target;
    if (!input.matches('[data-uppercase]')) return;
    const start = input.selectionStart, end = input.selectionEnd;
    input.value = input.value.toUpperCase();
    if (start !== null) input.setSelectionRange(start, end);
  });
  document.addEventListener('click', (event) => {
    const menu = document.querySelector('[data-profile-menu]');
    if (menu?.open && !menu.contains(event.target)) menu.open = false;
  });
  document.addEventListener('keydown', (event) => {
    const menu = document.querySelector('[data-profile-menu]');
    if (event.key === 'Escape' && menu?.open) {
      menu.open = false;
      menu.querySelector('summary').focus();
      event.preventDefault();
    }
  });
  document.addEventListener('change', (event) => {
    if (event.target.matches('[name="recurrence_type"]')) updateRecurrence(event.target);
  });
  document.addEventListener('click', async (event) => {
    const disclosure = event.target.closest('[data-disclosure]');
    if (disclosure) {
      const target = document.querySelector(disclosure.dataset.disclosureTarget);
      if (target) { const open = disclosure.getAttribute('aria-expanded') !== 'true'; target.classList.toggle('show', open); disclosure.setAttribute('aria-expanded', String(open)); }
    }
    if (event.target.closest('#add-meaning-btn')) { addMeaning(); document.querySelector('#meanings-list .meaning-row:last-child input')?.focus(); }
    const remove = event.target.closest('[data-remove-meaning]');
    if (remove) { remove.closest('.meaning-row').remove(); if (!document.querySelector('#meanings-list .meaning-row')) addMeaning(); }
    const weekdays = event.target.closest('[data-weekday-action]');
    if (weekdays) weekdays.closest('form').querySelectorAll('#weekday-checkboxes input').forEach((input) => { input.checked = weekdays.dataset.weekdayAction === 'select-all'; });
    if (event.target.closest('[data-close-sheet]') && !requestPending) sheet.close();
    const link = event.target.closest('a[href]');
    if (!link || event.defaultPrevented || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.button !== 0 || link.target || link.hasAttribute('download') || !sheet) return;
    const url = new URL(link.href);
    if (url.origin !== location.origin || !/^\/(tasks|recurring-tasks|project-tasks)\/(create\/|\d+\/update\/)$/.test(url.pathname)) return;
    if (document.querySelector('[data-set-form][data-dirty="true"], [data-shopping-dirty="true"]')) return;
    event.preventDefault();
    if (requestPending) return;
    requestPending = true;
    try {
      const response = await fetch(url, { credentials: 'same-origin' });
      if (!response.ok) throw new Error();
      const doc = new DOMParser().parseFromString(await response.text(), 'text/html');
      const content = doc.querySelector('[data-mission-editor]');
      if (!content) { location.assign(response.url); return; }
      sheetOpener = link;
      sheet.querySelector('[data-sheet-content]').replaceChildren(content);
      initialize(sheet);
      sheet.showModal(); document.body.classList.add('sheet-open');
    } catch { toast('Não foi possível abrir o formulário. Tente novamente.'); }
    finally { requestPending = false; }
  });
  if (sheet) {
    sheet.addEventListener('close', () => { document.body.classList.remove('sheet-open'); sheetOpener?.focus(); });
    sheet.addEventListener('cancel', (event) => { if (requestPending) event.preventDefault(); });
  }
  document.addEventListener('submit', async (event) => {
    const form = event.target;
    const inSheet = sheet?.open && sheet.contains(form);
    const inline = form.matches('[data-set-form], [data-shopping-progress]');
    if (!inSheet && !inline) return;
    event.preventDefault();
    if (form.getAttribute('aria-busy') === 'true') return;
    const data = new FormData(form);
    if (event.submitter?.name) data.append(event.submitter.name, event.submitter.value);
    const buttons = [...form.querySelectorAll('button[type="submit"], button:not([type])')];
    const focusId = document.activeElement?.id;
    form.setAttribute('aria-busy', 'true'); buttons.forEach((button) => { button.disabled = true; });
    if (inSheet) requestPending = true;
    document.dispatchEvent(new CustomEvent('app:save-started', { detail: { form } }));
    let updated = false;
    try {
      // The header retains the server's established fragment contract; no client library is loaded.
      const response = await fetch(form.action, { method: 'POST', body: data, credentials: 'same-origin', headers: inline ? { 'HX-Request': 'true' } : {} });
      if (!response.ok) throw new Error();
      const redirect = response.headers.get('HX-Redirect');
      if (redirect || response.redirected) {
        if (form.matches('[data-shopping-progress]')) form.dataset.shoppingDirty = 'false';
        if (form.matches('[data-set-form]')) delete form.dataset.dirty;
        location.assign(redirect || response.url); return;
      }
      const doc = new DOMParser().parseFromString(await response.text(), 'text/html');
      if (inSheet) {
        const content = doc.querySelector('[data-mission-editor]');
        if (!content) throw new Error();
        sheet.querySelector('[data-sheet-content]').replaceChildren(content); initialize(sheet);
        sheet.querySelector('[aria-invalid="true"], .errorlist, input:not([type="hidden"])')?.focus();
      } else if (form.matches('[data-set-form]')) {
        const content = doc.querySelector('.workout-set');
        if (!content) throw new Error();
        form.closest('.workout-set').replaceWith(content);
        const progress = doc.querySelector('[data-session-progress]');
        if (progress) document.getElementById(progress.id)?.replaceWith(progress);
        initialize(content);
        if (focusId) document.getElementById(focusId)?.focus({ preventScroll: true });
        else content.querySelector('button')?.focus({ preventScroll: true });
      } else {
        const content = doc.querySelector('[data-shopping-section]');
        if (!content) throw new Error();
        document.getElementById('page-content').replaceChildren(content); initialize(content);
        content.querySelector('[data-shopping-progress] button')?.focus({ preventScroll: true });
      }
      updated = true;
      const triggers = response.headers.get('HX-Trigger-After-Swap');
      if (triggers) Object.entries(JSON.parse(triggers)).forEach(([name, detail]) => document.dispatchEvent(new CustomEvent(name, { detail })));
    } catch {
      if (!updated) {
        feedback(form, 'Não foi possível salvar. Confira a conexão e tente novamente. Os dados continuam nos campos.');
        document.dispatchEvent(new CustomEvent('app:save-failed', { detail: { form } }));
      }
    } finally {
      form.removeAttribute('aria-busy'); buttons.forEach((button) => { button.disabled = false; });
      requestPending = false;
    }
  });
  initialize();
  // A direct link or validation response uses the same bottom-sheet component.
  const directEditor = document.querySelector('#page-content [data-mission-editor]');
  if (directEditor && sheet) {
    const cancel = directEditor.querySelector('.form-actions a')?.href;
    sheet.querySelector('[data-sheet-content]').replaceChildren(directEditor);
    sheet.showModal(); document.body.classList.add('sheet-open');
    sheet.addEventListener('close', () => { location.assign(cancel || '/tasks/list/'); }, { once: true });
  }
})();
