from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import TemplateView

from tasks.presentation import get_daily_category_context
from tasks.services import get_skill_progress, get_today_mission_context
from app.utils import PageTitleMixin, htmx_redirect, is_htmx_request

from . import forms, services


class DashboardView(PageTitleMixin, LoginRequiredMixin, TemplateView):
    template_name = 'progress/dashboard.html'
    page_title = 'BTY - Dashboard'

    def get(self, request, *args, **kwargs):
        # The new shell has no HTMX dependency; leave the legacy shell on entry.
        if is_htmx_request(request):
            return htmx_redirect(request.get_full_path())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        default_start_date, default_end_date = forms.DashboardFilterForm.default_range()

        if self.request.GET:
            filter_form = forms.DashboardFilterForm(self.request.GET)
        else:
            filter_form = forms.DashboardFilterForm(initial={
                'start_date': default_start_date,
                'end_date': default_end_date,
            })

        if filter_form.is_bound and filter_form.is_valid():
            start_date = filter_form.cleaned_data.get('start_date')
            end_date = filter_form.cleaned_data.get('end_date')
        else:
            start_date, end_date = default_start_date, default_end_date

        mission_context = get_today_mission_context()
        dashboard_context = services.get_dashboard_context(
            start_date=start_date,
            end_date=end_date,
        )

        context.update(dashboard_context)
        category_context, daily_tasks = get_daily_category_context(mission_context, self.request.GET)
        context.update(category_context)
        context['daily_tasks'] = daily_tasks.filter(skipped_in__isnull=True).order_by('completed_at', '-priority', 'title')[:6]
        hour = timezone.localtime().hour
        context['greeting'] = 'Bom dia' if hour < 12 else ('Boa tarde' if hour < 18 else 'Boa noite')
        context['filter_form'] = filter_form
        return context


class EvolutionView(DashboardView):
    template_name = 'progress/evolution.html'
    page_title = 'BTY - Evolução'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skills'] = get_skill_progress()
        return context
