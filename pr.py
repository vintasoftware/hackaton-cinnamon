import requests
import re

from issues.models import PullRequest, Issue

repo_owner = 'evansd'
repo = 'whitenoise'
prs_url = 'https://api.github.com/repos/%s/%s/pulls?state=all' % (repo_owner, repo)

response = requests.get(prs_url)
pr_list = response.json()
pr_issue_dict = {}

for pr in pr_list:
    pr_body = pr['body']
    issue_numbers = []

    matches = list(re.finditer(r'#(\d+)', pr_body))
    if matches:
        issue_numbers += [issues.groups()[0] for issues in matches]

    matches = list(re.finditer(r'#(\d+)', pr['title']))
    if matches:
        issue_numbers += [issues.groups()[0] for issues in matches]

    if not issue_numbers:
        continue

    issues = Issue.objects.filter(number__in=issue_numbers)
    p, _ = PullRequest.objects.get_or_create(number=pr['number'],
                                             defaults={
                                                'title': pr['title'],
                                                'body': pr['body'],
                                                'repo_owner': repo_owner,
                                                'repo': repo,
                                                'raw': str(pr)
                                             })
    p.issues = issues

    pr_issue_dict[pr['number']] = {
        'pr': pr['title'],
        'text': pr['body'],
        'issue_numbers': [i[1:] for i in issue_numbers]
    }


import pprint
pprint.pprint(pr_issue_dict)
