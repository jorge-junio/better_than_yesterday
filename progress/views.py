from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from . import forms, services
from app.utils import HtmxTemplateMixin, PageTitleMixin


class DashboardView(HtmxTemplateMixin, PageTitleMixin, LoginRequiredMixin, TemplateView):
    template_name = 'progress/dashboard.html'
    htmx_template_name = 'progress/partials/dashboard_content.html'
    page_title = 'BTY - Dashboard'

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

        dashboard_context = services.get_dashboard_context(
            start_date=start_date,
            end_date=end_date,
        )

        context.update(dashboard_context)
        context['filter_form'] = filter_form
        return context
