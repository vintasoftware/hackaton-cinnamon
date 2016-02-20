from django.views import generic

class LandingPageView(generic.TemplateView):
    template_name = 'core/landing.html'
