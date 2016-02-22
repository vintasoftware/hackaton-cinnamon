from django.views import generic

from accounts.models import Repos


class LandingPageView(generic.TemplateView):
    template_name = 'core/landing.html'


class LoadingRepoView(generic.DetailView):
    model = Repos
    template_name = 'core/loading.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context
