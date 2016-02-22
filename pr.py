import requests
import re
import json
from requests.auth import HTTPBasicAuth

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.local")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
GITHUB_USER = os.environ['GITHUB_USER']
GITHUB_KEY = os.environ['GITHUB_KEY']

from issues.models import PullRequest, Issue

repo_owner = 'omab'
repo = 'python-social-auth'
prs_url = 'https://api.github.com/repos/%s/%s/pulls' % (repo_owner, repo)

page = 1
response = requests.get(prs_url, params={'state': 'all', 'page': page},
                        auth=HTTPBasicAuth(GITHUB_USER, GITHUB_KEY))
pr_list = response.json()
# pr_issue_dict = {}

while pr_list:
    print('Page', page)
    for pr in pr_list:
        pr_body = pr['body'] or ""
        issue_numbers = []

        matches = list(re.finditer(r'#(\d+)', pr_body))
        if matches:
            issue_numbers += [issues.groups()[0] for issues in matches]

        matches = list(re.finditer(r'#(\d+)', pr['title']))
        if matches:
            issue_numbers += [issues.groups()[0] for issues in matches]

        p, _ = PullRequest.objects.get_or_create(number=pr['number'],
                                                 defaults={
                                                    'title': pr['title'],
                                                    'body': pr['body'] or '',
                                                    'author': pr['user']['login'],
                                                    'repo_owner': repo_owner,
                                                    'repo': repo,
                                                    'raw': json.dumps(pr)
                                                 })
        if issue_numbers:
            issues = Issue.objects.filter(number__in=issue_numbers)
            p.issues = issues
        print("saving PR#", pr['number'])
        # pr_issue_dict[pr['number']] = {
        #     'pr': pr['title'],
        #     'text': pr['body'],
        #     'issue_numbers': [i[1:] for i in issue_numbers]
        # }
    page += 1
    response = requests.get(prs_url, params={'state': 'all', 'page': page},
                            auth=HTTPBasicAuth(GITHUB_USER, GITHUB_KEY))
    pr_list = response.json()


# import pprint
# pprint.pprint(pr_issue_dict)
