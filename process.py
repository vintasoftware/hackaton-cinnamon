import os
import json
import re
from requests.auth import HTTPBasicAuth
from django.utils.dateparse import parse_datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.local")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import requests
from issues.models import *
from accounts.models import Repos

for repo in Repos.objects.filter(is_done=False):
    repo_obj = repo
    if repo.parent_repo:
        repo_owner = repo.parent_repo_owner
        repo = repo.parent_repo
    else:
        repo_owner = repo.owner
        repo = repo.name
    if Issue.objects.filter(repo=repo, repo_owner=repo_owner).exists():
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
                repo=repo,
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
                issues = Issue.objects.filter(repo_owner=repo_owner,
                                              repo=repo,
                                              number__in=issue_numbers)
                p.issues = issues

                response_files = requests.get(pr['url'] + '/files',
                                              auth=HTTPBasicAuth(GITHUB_USER, GITHUB_KEY))
                files = response_files.json()
                p.files = [File.objects.create(filename=f['filename']) for f in files]

        page += 1
        response = requests.get(prs_url, params={'state': 'all', 'page': page},
                                auth=HTTPBasicAuth(GITHUB_USER, GITHUB_KEY))
        pr_list = response.json()
    repo_obj.is_done = True
    repo_obj.save()

    print("Done!")
