(() => {
  const picker = document.querySelector('[data-photo-picker]');
  if (!picker || typeof URL.createObjectURL !== 'function') return;
  const form = picker.querySelector('[data-photo-upload]');
  const input = form.querySelector('input[name="photo"]');
  const preview = picker.querySelector('[data-photo-preview]');
  const status = picker.querySelector('#photo-preview-status');
  const save = picker.querySelector('[data-photo-save]');
  const cancel = picker.querySelector('[data-photo-cancel]');
  const remove = form.querySelector('input[name="remove_photo"]');
  if (!input || !preview || !status || !save || !cancel || !remove) return;

  const savedSrc = preview.getAttribute('src');
  const savedAlt = preview.alt;
  const open = picker.querySelector('[data-photo-open]');
  const dialog = picker.querySelector('[data-photo-dialog]');
  const expanded = picker.querySelector('[data-photo-expanded]');
  const maxBytes = Number(input.dataset.maxBytes);
  const maxPixels = Number(input.dataset.maxPixels);
  let sequence = 0;
  let objectUrl = null;
  let previewedFile = null;

  const descriptions = new Set((input.getAttribute('aria-describedby') || '').split(/\s+/).filter(Boolean));
  descriptions.add(status.id);
  input.setAttribute('aria-describedby', [...descriptions].join(' '));

  function releaseUrl() {
    if (objectUrl) URL.revokeObjectURL(objectUrl);
    objectUrl = null;
  }

  function restoreSavedPhoto() {
    if (preview.getAttribute('src') !== savedSrc) preview.src = savedSrc;
    preview.alt = savedAlt;
  }

  function reset() {
    sequence += 1;
    releaseUrl();
    restoreSavedPhoto();
    previewedFile = null;
    input.value = '';
    input.setCustomValidity('');
    input.removeAttribute('aria-invalid');
    save.disabled = false;
    cancel.hidden = true;
    cancel.textContent = remove.checked ? 'Desfazer remoção' : 'Descartar seleção';
    if (open) open.classList.toggle('photo-pending-removal', remove.checked);
    status.textContent = remove.checked
      ? 'Foto será removida ao salvar.'
      : '';
  }

  function reject(message) {
    reset();
    input.setCustomValidity(message);
    input.setAttribute('aria-invalid', 'true');
    save.disabled = true;
    cancel.hidden = false;
    status.textContent = message;
  }

  input.addEventListener('change', async () => {
    const file = input.files[0];
    const current = ++sequence;
    releaseUrl();
    restoreSavedPhoto();
    previewedFile = null;
    input.setCustomValidity('');
    input.removeAttribute('aria-invalid');
    save.disabled = true;
    cancel.hidden = !file;
    if (!file) {
      reset();
      return;
    }
    remove.checked = false;
    if (open) open.classList.remove('photo-pending-removal');
    if (file.size > maxBytes) {
      reject('A foto deve ter no máximo 5 MB.');
      return;
    }
    status.textContent = 'Preparando pré-visualização…';
    try {
      const header = new Uint8Array(await file.slice(0, 8).arrayBuffer());
      if (current !== sequence) return;
      const jpeg = header[0] === 255 && header[1] === 216 && header[2] === 255;
      const png = [137, 80, 78, 71, 13, 10, 26, 10].every((value, index) => header[index] === value);
      if (!jpeg && !png) {
        reject('Selecione uma imagem JPEG ou PNG válida.');
        return;
      }
      objectUrl = URL.createObjectURL(file);
      const candidateUrl = objectUrl;
      const image = new Image();
      image.onload = () => {
        if (current !== sequence) return;
        if (!image.naturalWidth || !image.naturalHeight
            || image.naturalWidth * image.naturalHeight > maxPixels) {
          reject('A foto deve ter até 20 megapixels.');
          return;
        }
        preview.src = candidateUrl;
        preview.alt = 'Pré-visualização da foto selecionada';
        previewedFile = file;
        save.disabled = false;
        status.textContent = 'Nova foto · Salve para confirmar.';
      };
      image.onerror = () => {
        if (current === sequence) reject('Não foi possível abrir esta foto. Escolha outro JPEG ou PNG.');
      };
      image.src = candidateUrl;
    } catch {
      if (current === sequence) reject('Não foi possível abrir esta foto. Selecione o arquivo novamente.');
    }
  });

  remove.addEventListener('change', reset);
  form.addEventListener('submit', (event) => {
    if (input.files[0] && (!previewedFile || previewedFile !== input.files[0])) {
      event.preventDefault();
      input.reportValidity();
    }
  });
  if (open && dialog && expanded && typeof dialog.showModal === 'function') {
    const edit = picker.querySelector('[data-photo-edit]');
    const deletePhoto = picker.querySelector('[data-photo-delete]');
    const close = picker.querySelector('[data-photo-close]');
    const field = picker.querySelector('[data-photo-field]');
    const removalField = picker.querySelector('[data-photo-remove-field]');
    const hint = picker.querySelector('[data-photo-hint]');
    if (edit && deletePhoto && close && field && removalField && hint) {
      dialog.hidden = false;
      open.disabled = false;
      field.hidden = true;
      removalField.hidden = true;
      hint.hidden = false;
      const quickEdit = picker.querySelector('[data-photo-quick-edit]');
      if (quickEdit) {
        quickEdit.disabled = false;
        quickEdit.addEventListener('click', () => input.click());
      }
      open.addEventListener('click', () => {
        expanded.src = preview.src;
        dialog.showModal();
      });
      close.addEventListener('click', () => dialog.close());
      dialog.addEventListener('close', () => expanded.removeAttribute('src'));
      edit.addEventListener('click', () => {
        dialog.close();
        input.click();
      });
      deletePhoto.addEventListener('click', () => {
        remove.checked = true;
        reset();
        // Permitir desfazer a remoção antes de salvar.
        cancel.hidden = false;
        dialog.close();
      });
    }
  }
  cancel.addEventListener('click', () => {
    remove.checked = false;
    reset();
  });
  window.addEventListener('pagehide', () => {
    if (dialog && dialog.open) dialog.close();
    reset();
  });
  save.disabled = false;
})();
