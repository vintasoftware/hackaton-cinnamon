import os
import json
from requests.auth import HTTPBasicAuth
from django.utils.dateparse import parse_datetime
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.local")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import requests
from issues.models import *

repo_owner = 'aericson'
repo = 'python-social-auth'
issues_url = 'https://api.github.com/repos/%s/%s/issues' % (repo_owner, repo)
GITHUB_USER = os.environ['GITHUB_USER']
GITHUB_KEY = os.environ['GITHUB_KEY']

# get new issues

since = Issue.objects.order_by('-updated_at').first().updated_at + timedelta(seconds=1)
page = 1
issues_response = requests.get(issues_url, params={'state': 'open', 'page': page,
                                                   'since': since.isoformat()},
                               auth=HTTPBasicAuth(GITHUB_USER, GITHUB_KEY))
issue_list = issues_response.json()
while issue_list:
    print("Found new issue")
    for gh_issue in issue_list:
        issue, is_new_issue = Issue.objects.get_or_create(
            number=gh_issue['number'],
            repo_owner=repo_owner,
            repo=repo,
            defaults={
                'title': gh_issue['title'],
                'body': gh_issue['body'] or '',
                'repo_owner': repo_owner,
                'repo': repo,
                'raw': json.dumps(gh_issue),
                'updated_at': parse_datetime(gh_issue['updated_at']),
                'answered': False,
            })
    page += 1
    issues_response = requests.get(issues_url, params={'state': 'open', 'page': page,
                                                       'since': since.isoformat()},
                                   auth=HTTPBasicAuth(GITHUB_USER, GITHUB_KEY))
    issue_list = issues_response.json()

for issue in Issue.objects.filter(answered=False):
    print("would answer", issue)
