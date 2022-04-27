from django.views import generic


class Index(generic.TemplateView):
    """トップページ"""
    template_name = 'common/index.html'
