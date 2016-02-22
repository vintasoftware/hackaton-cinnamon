import os
import json
from requests.auth import HTTPBasicAuth
from django.utils.dateparse import parse_datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.local")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import requests
from issues.models import *

for repo in Repos.objects.all():
    if repo.parent_repo:
        repo_owner = repo.parent_repo_owner
        repo = repo.parent_repo
    else:
        repo_owner = repo.owner
        repo = repo.name
    if Issues.objects.filter(repo=repo, repo_owner=repo_owner).exists():
        continue

    issues_url = 'https://api.github.com/repos/%s/%s/issues' % (repo_owner, repo)
    GITHUB_USER = os.environ['GITHUB_USER']
    GITHUB_KEY = os.environ['GITHUB_KEY']

    page = 1
    issues_response = requests.get(issues_url, params={'state': 'all', 'page': page},
                                   auth=HTTPBasicAuth(GITHUB_USER, GITHUB_KEY))
    issue_list = issues_response.json()
    while issue_list:
        print('Page', page)
        for gh_issue in issue_list:
            print('Inserting', gh_issue['number'])
            issue, is_new_issue = Issue.objects.get_or_create(
                number=gh_issue['number'],
                repo_owner=repo_owner,
                repo=repo
                defaults={
                    'title': gh_issue['title'],
                    'body': gh_issue['body'] or '',
                    'repo_owner': repo_owner,
                    'repo': repo,
                    'raw': json.dumps(gh_issue),
                    'updated_at': parse_datetime(gh_issue['updated_at']),
                    'answered': True,
                })

        page += 1
        issues_response = requests.get(issues_url, params={'state': 'all', 'page': page},
                                       auth=HTTPBasicAuth(GITHUB_USER, GITHUB_KEY))
        issue_list = issues_response.json()

    print("Done!")
