
import requests

from django.views.generic import ListView

from allauth.socialaccount.models import SocialToken

from accounts.models import Repos


class RepoListView(ListView):
    model = Repos
    template_name = 'accounts/repo_list.html'

    def get_queryset(self):
        user = self.request.user
        return Repos.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super(RepoListView, self).get_context_data(**kwargs)
        socialtoken = SocialToken.objects.get(account__user=self.request.user)
        params = {'access_token': socialtoken}
        all_repos = requests.get('https://api.github.com/user/repos', params=params).json()
        repos_added = Repos.objects.all().values_list('name', flat=True)
        context['repos_not_added'] = [r for r in all_repos if r['name'] not in repos_added]
        return context
