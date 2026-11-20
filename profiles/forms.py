from io import BytesIO
import warnings

from django import forms
from PIL import Image, ImageOps, UnidentifiedImageError


class ProfilePhotoForm(forms.Form):
    photo = forms.FileField(
        label='Foto de perfil', required=False,
        widget=forms.FileInput(attrs={'accept': 'image/jpeg,image/png', 'data-photo-input': '', 'data-max-bytes': 5 * 1024 * 1024, 'data-max-pixels': 20_000_000}),
    )
    remove_photo = forms.BooleanField(label='Remover foto', required=False)

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if not photo:
            return None
        if photo.size > 5 * 1024 * 1024:
            raise forms.ValidationError('A foto deve ter no máximo 5 MB.')
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('error', Image.DecompressionBombWarning)
                with Image.open(photo) as source:
                    if source.format not in ('JPEG', 'PNG'):
                        raise forms.ValidationError('Selecione uma imagem JPEG ou PNG.')
                    if source.width * source.height > 20_000_000:
                        raise forms.ValidationError('A foto deve ter até 20 megapixels.')
                    source.load()
                    image = ImageOps.exif_transpose(source).convert('RGBA')
                    image.thumbnail((512, 512))
                    background = Image.new('RGB', image.size, 'white')
                    background.paste(image, mask=image.getchannel('A'))
                    output = BytesIO()
                    background.save(output, format='JPEG', quality=85)
                    return output.getvalue()
        except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError, Image.DecompressionBombWarning):
            raise forms.ValidationError('Não foi possível ler a imagem. Escolha uma foto JPEG ou PNG válida.')

    def clean(self):
        data = super().clean()
        if data.get('photo') and data.get('remove_photo'):
            raise forms.ValidationError('Escolha uma nova foto ou remova a atual, uma opção por vez.')
        return data
