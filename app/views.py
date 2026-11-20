from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.views.decorators.http import require_http_methods, require_safe

from profiles.forms import ProfilePhotoForm
from profiles.models import ProfilePhoto
from django.shortcuts import redirect, render

from .navigation import MENU_SECTIONS, get_menu_sections
from .utils import is_htmx_request


@login_required(login_url='login')
def home(request):
    return redirect('dashboard')


@login_required(login_url='login')
def menu_section(request, section):
    if section not in {item[0] for item in MENU_SECTIONS}:
        raise Http404
    selected = next((item for item in get_menu_sections(request.user) if item['slug'] == section), None)
    if selected is None:
        raise PermissionDenied
    template = 'menus/section_content.html' if is_htmx_request(request) else 'menus/section.html'
    return render(request, template, {'section': selected, 'page_title': f"BTY - {selected['label']}"})


@login_required(login_url='login')
def character(request):
    from tasks.services import get_skill_progress, get_today_mission_context
    return render(request, 'life_rpg/character.html', {
        'mission': get_today_mission_context(), 'skills': get_skill_progress(),
        'page_title': 'BTY - Personagem',
    })


@login_required(login_url='login')
@require_http_methods(['GET', 'POST'])
def profile(request):
    form = ProfilePhotoForm(request.POST if request.method == 'POST' else None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        if form.cleaned_data['remove_photo']:
            ProfilePhoto.objects.filter(user=request.user).delete()
            messages.success(request, 'Foto removida.')
        elif form.cleaned_data['photo']:
            ProfilePhoto.objects.update_or_create(user=request.user, defaults={'image': form.cleaned_data['photo']})
            messages.success(request, 'Foto atualizada.')
        return redirect('profile')
    return render(request, 'life_rpg/profile.html', {'page_title': 'BTY - Perfil', 'photo_form': form})


@login_required(login_url='login')
@require_safe
def profile_photo(request):
    photo = ProfilePhoto.objects.filter(user=request.user).first()
    if photo:
        response = HttpResponse(bytes(photo.image), content_type='image/jpeg')
    else:
        response = HttpResponse('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128"><rect width="128" height="128" rx="64" fill="#292435"/><g fill="none" stroke="#c4b5fd" stroke-width="6"><circle cx="64" cy="45" r="20"/><path d="M26 108v-9a38 38 0 0 1 76 0v9"/></g></svg>', content_type='image/svg+xml')
    response['Cache-Control'] = 'private, no-store'
    response['X-Content-Type-Options'] = 'nosniff'
    return response


@login_required(login_url='login')
def areas(request):
    area_order = ('workouts', 'english', 'shopping', 'projects')
    available_sections = {section['slug']: section for section in get_menu_sections(request.user)}
    sections = [available_sections[slug] for slug in area_order if slug in available_sections]
    return render(request, 'life_rpg/areas.html', {'page_title': 'BTY - Áreas', 'area_sections': sections})
