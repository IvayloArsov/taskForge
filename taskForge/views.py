from django.views.generic.base import TemplateView


class Index(TemplateView):
    template_name = 'common/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AboutView(TemplateView):
    template_name = 'common/about.html'

class ContactView(TemplateView):
    template_name = 'common/contact.html'
