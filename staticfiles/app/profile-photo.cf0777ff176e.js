(() => {
  const form = document.querySelector('[data-photo-form]');
  if (!form) return;
  const input = form.querySelector('[data-photo-input]');
  const remove = form.querySelector('[name="remove_photo"]');
  const preview = document.querySelector('[data-photo-preview]');
  const original = preview.src;
  const dialog = document.querySelector('[data-photo-dialog]');
  const expanded = dialog.querySelector('[data-photo-expanded]');
  const status = form.querySelector('[data-photo-status]');
  const discard = form.querySelector('[data-photo-discard]');
  let objectUrl;
  const clearUrl = () => { if (objectUrl) URL.revokeObjectURL(objectUrl); objectUrl = null; };
  const reset = () => {
    clearUrl(); input.value = ''; remove.checked = false; preview.src = original;
    status.textContent = ''; discard.hidden = true;
  };
  input.addEventListener('change', () => {
    const file = input.files[0];
    if (!file) return;
    if (!['image/jpeg', 'image/png'].includes(file.type) || file.size > 5 * 1024 * 1024) {
      reset(); status.textContent = 'Selecione uma foto JPEG ou PNG de até 5 MB.'; return;
    }
    clearUrl(); objectUrl = URL.createObjectURL(file); preview.src = objectUrl;
    remove.checked = false; discard.hidden = false;
    status.textContent = 'Prévia da nova foto. Clique em Salvar foto para confirmar.';
  });
  remove.addEventListener('change', () => {
    if (remove.checked) {
      clearUrl(); input.value = ''; preview.src = original; discard.hidden = false;
      status.textContent = 'Clique em Salvar foto para confirmar a remoção.';
    } else reset();
  });
  discard.addEventListener('click', reset);
  document.querySelector('[data-photo-open]').addEventListener('click', () => {
    expanded.src = preview.src; dialog.showModal();
  });
  dialog.querySelector('[data-photo-close]').addEventListener('click', () => dialog.close());
  dialog.querySelector('[data-photo-edit]').addEventListener('click', () => { dialog.close(); input.click(); });
  dialog.querySelector('[data-photo-remove]').addEventListener('click', () => {
    dialog.close(); remove.checked = true; remove.dispatchEvent(new Event('change'));
  });
  window.addEventListener('pagehide', clearUrl);
})();
