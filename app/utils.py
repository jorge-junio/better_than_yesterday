from django.http import HttpResponse
from django.utils.formats import number_format


def is_htmx_request(request):
    return request.headers.get('HX-Request') == 'true'


def htmx_redirect(url):
    response = HttpResponse(status=204)
    response['HX-Redirect'] = url
    return response


def build_querystring(request, exclude=None):
    exclude = set(exclude or [])
    params = request.GET.copy()
    for key in exclude:
        params.pop(key, None)
    return params.urlencode()


class HtmxTemplateMixin:
    htmx_template_name = None

    def get_template_names(self):
        if is_htmx_request(self.request) and self.htmx_template_name:
            return [self.htmx_template_name]
        return super().get_template_names()


class PageTitleMixin:
    page_title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.page_title:
            context['page_title'] = self.page_title
        return context


def format_money(value):
    return number_format(value, decimal_pos=2, force_grouping=True)
