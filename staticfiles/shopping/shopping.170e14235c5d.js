(function () {
  function pendingForm() {
    return document.querySelector('form[data-shopping-progress][data-shopping-dirty="true"]');
  }

  document.addEventListener('input', function (event) {
    const form = event.target.closest('form[data-shopping-progress]');
    if (form) form.dataset.shoppingDirty = 'true';
  });

  document.addEventListener('submit', function (event) {
    if (event.target.matches('form[data-shopping-progress]')) {
      event.target.dataset.shoppingDirty = 'false';
    }
  }, true);

  document.addEventListener('htmx:afterRequest', function (event) {
    const form = event.detail.elt;
    if (form.matches && form.matches('form[data-shopping-progress]') && !event.detail.successful) {
      form.dataset.shoppingDirty = 'true';
      const feedback = form.querySelector('[data-shopping-error]');
      if (feedback) feedback.hidden = false;
    }
  });

  document.addEventListener('click', function (event) {
    const link = event.target.closest('a[href]');
    const form = pendingForm();
    if (!link || !form || link.getAttribute('href').startsWith('#')) return;
    if (!window.confirm('Há quantidades ainda não salvas. Sair sem salvar?')) {
      event.preventDefault();
      event.stopImmediatePropagation();
    } else {
      form.dataset.shoppingDirty = 'false';
    }
  }, true);

  window.addEventListener('beforeunload', function (event) {
    if (!pendingForm()) return;
    event.preventDefault();
    event.returnValue = '';
  });
}());
