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

from issues.models import PullRequest, Issue, File

repo_owner = 'omab'
repo = 'python-social-auth'
prs_url = 'https://api.github.com/repos/%s/%s/pulls' % (repo_owner, repo)

page = 1
response = requests.get(prs_url, params={'state': 'all', 'page': page},
                        auth=HTTPBasicAuth(GITHUB_USER, GITHUB_KEY))
pr_list = response.json()

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

        if issue_numbers:
            p, _ = PullRequest.objects.get_or_create(number=pr['number'],
                                                     repo_owner=repo_owner,
                                                     repo=repo,
                                                     defaults={
                                                        'title': pr['title'],
                                                        'body': pr['body'] or '',
                                                        'author': pr['user']['login'],
                                                        'repo_owner': repo_owner,
                                                        'repo': repo,
                                                        'raw': json.dumps(pr)
                                                     })
            issues = Issue.objects.filter(number__in=issue_numbers)
            p.issues = issues

            response_files = requests.get(pr['url'] + '/files',
                                          auth=HTTPBasicAuth(GITHUB_USER, GITHUB_KEY))
            files = response_files.json()
            p.files = [File.objects.create(filename=f['filename']) for f in files]

    page += 1
    response = requests.get(prs_url, params={'state': 'all', 'page': page},
                            auth=HTTPBasicAuth(GITHUB_USER, GITHUB_KEY))
    pr_list = response.json()
