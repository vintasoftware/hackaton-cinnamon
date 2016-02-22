from django.views import generic

class LandingPageView(generic.TemplateView):
    template_name = 'core/landing.html'


class LoadingTemplateView(generic.TemplateView):
     template_name = 'core/loading.html'
