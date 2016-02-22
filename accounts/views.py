
import json
import requests

from django.http import HttpResponse
from django.views.generic import ListView, CreateView, DeleteView

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
        context['repos_not_added'] = [(json.dumps(r), r['name']) for r in all_repos if r['name'] not in repos_added and r['private'] is False]
        context['all_repos'] = [(json.dumps(r), r['name']) for r in all_repos if r['private'] is False]
        context['added_repos_names'] = repos_added
        return context


class RepoCreateView(CreateView):
    model = Repos
    fields = ['name', 'html_url']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        socialtoken = SocialToken.objects.get(account__user=self.request.user)
        params = {'access_token': socialtoken}
        repo_details = requests.get('https://api.github.com/repos/aericson/python-social-auth', params=params).json()
        if repo_details.get('parent'):
            self.object.parent_repo_owner = repo_details['parent']['owner']['login']
            self.object.parent_repo = repo_details['parent']['name']
            self.object.owner = repo_details['owner']['login']
            self.object.creating = True
        self.object.save()
        return HttpResponse(json.dumps(form.data), content_type="application/json")


class RepoDeleteView(DeleteView):
    model = Repos

    def delete(self, request, *args, **kwargs):
        name = self.request.POST.get('name')
        repo = Repos.objects.get(user=self.request.user, name=name)
        repo.delete()
        return HttpResponse(json.dumps("'ahn': 'heuia'"), content_type="application/json")
