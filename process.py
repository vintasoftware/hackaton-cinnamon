import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.local")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import requests
from issues.models import *

issues_url = 'https://api.github.com/repos/omab/python-social-auth/issues'
repo_owner = 'omab'
repo = 'python-social-auth'

page = 1
issues_response = requests.get(issues_url, params={'state': 'all', 'page': page})
issue_list = issues_response.json()
while issue_list:
    print('Page', page)
    for gh_issue in issue_list:
        print('Inserting', gh_issue['number'])
        issue, is_new_issue = Issue.objects.get_or_create(
            number=gh_issue['number'],
            defaults={
                'title': gh_issue['title'],
                'body': gh_issue['body'] or '',
                'repo_owner': repo_owner,
                'repo': repo,
                'raw': str(gh_issue)
            })

    page += 1
    issues_response = requests.get(issues_url, params={'state': 'all', 'page': page})
    issue_list = issues_response.json()

print("Done!")
