(function () {
  function pendingForm() {
    return document.querySelector('form[data-shopping-progress][data-shopping-dirty="true"]');
  }

  document.addEventListener('input', function (event) {
    const form = event.target.closest('form[data-shopping-progress]');
    if (form) form.dataset.shoppingDirty = 'true';
  });

  document.addEventListener('app:save-failed', function (event) {
    const form = event.detail.form;
    if (form.matches('[data-shopping-progress]')) {
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
