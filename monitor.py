import os
import json
from requests.auth import HTTPBasicAuth
from django.utils.dateparse import parse_datetime
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.local")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import requests
from accounts.models import Repos
from issues.utils.similar import find_similiar
from issues.models import *


for repo in Repos.objects.all():
    repo_owner = repo.owner
    repo = repo.name

    issues_url = 'https://api.github.com/repos/%s/%s/issues' % (repo_owner, repo)
    GITHUB_USER = os.environ['GITHUB_USER']
    GITHUB_KEY = os.environ['GITHUB_KEY']

    params={'state': 'open', 'page': 1}

    # get new issues
    last_user = Issue.objects.filter(repo_owner=repo_owner, repo=repo
        ).order_by('-updated_at').first()
    if last_user:
        params['since'] = last_user.updated_at.isoformat()

    issues_response = requests.get(issues_url, params=params,
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
        params['page'] += 1
        issues_response = requests.get(issues_url, params=params,
                                       auth=HTTPBasicAuth(GITHUB_USER, GITHUB_KEY))
        issue_list = issues_response.json()

    prs_url = 'https://api.github.com/repos/%s/%s/pulls' % (repo_owner, repo)

    params['state'] = 'all'
    params['page'] = 1
    response = requests.get(prs_url, params=params,
                            auth=HTTPBasicAuth(GITHUB_USER, GITHUB_KEY))
    pr_list = response.json()

    while pr_list:
        print('Page', params['page'])
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

        params['page'] += 1
        response = requests.get(prs_url, params=params,
                                auth=HTTPBasicAuth(GITHUB_USER, GITHUB_KEY))
        pr_list = response.json()


for issue in Issue.objects.filter(answered=False):
    print(issue)
    repo = Repos.objects.get(owner=issue.repo_owner, name=issue.repo)
    if repo.parent_repo:
        similar_issues = find_similiar(issue, repo.parent_repo, repo.parent_repo_owner)
    else:
        similar_issues = find_similiar(issue, repo.name, repo.owner)
    suggested_users = set()
    suggested_files = set()
    for issue in similar_issues:
        for pr in issue.prs.all():
            suggested_users.add(pr.author)
            for f in pr.files.all():
                suggested_files.add(f.filename)
    print("would suggest:", similar_issues)
    print("would suggest:", suggested_files)
    print("would suggest:", suggested_users)
