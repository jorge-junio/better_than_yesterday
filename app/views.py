from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404
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
def profile(request):
    return render(request, 'life_rpg/profile.html', {'page_title': 'BTY - Perfil'})


@login_required(login_url='login')
def areas(request):
    return render(request, 'life_rpg/areas.html', {'page_title': 'BTY - Áreas'})
