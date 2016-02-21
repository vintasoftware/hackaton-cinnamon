import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.local")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import time
import requests
import re
from issues.models import *
import textrank

issues_url = 'https://api.github.com/repos/evansd/whitenoise/issues'
apikey = '213846289c43a4f637ae6eef1b8a08409680b3d9'
repo_owner = 'evansd'
repo = 'whitenoise'

page = 1
issues_response = requests.get(issues_url, params={'state': 'all', 'page': page})
issue_list = issues_response.json()
while issue_list:
    print('Page', page)
    for gh_issue in issue_list:
        while True:
            print('Processing', gh_issue['number'])
            issue, is_new_issue = Issue.objects.get_or_create(
                number=gh_issue['number'],
                defaults={
                    'title': gh_issue['title'],
                    'body': gh_issue['body'] or '',
                    'repo_owner': repo_owner,
                    'repo': repo,
                    'raw': str(gh_issue)
                })

            # add title and remove code blocks
            issue_body = issue.title + ' ' + \
                re.sub(r'```.+```', '', issue.body, flags=re.DOTALL)

            # get tags
            try:
                response = requests.post(
                    'https://api.monkeylearn.com/v2/extractors/ex_y7BPYzNG/extract/',
                    headers={
                        'Authorization': 'Token {}'.format(apikey)
                    },
                    params={
                        'max_keywords': 20,
                        'expand_acronyms': False
                    },
                    json={"text_list": [issue_body]})
            except Exception:
                print('Monkeylearn error!')
                import traceback
                traceback.print_exc()
                print(response.text)
            response_json = response.json()
            if 'result' not in response_json or \
               not response_json['result']:
                print("Failed getting tags for", issue.number)
                print("Got:")
                print(response_json)
                print("Sleeping...")
                time.sleep(60)
                print("Woke up! Will retry")
                continue  # try again
            keyword_list = response_json['result'][0]

            for keyword in keyword_list:
                if not is_new_issue:
                    Tag.objects.filter(issue=issue).delete()
                Tag.objects.create(
                    issue=issue,
                    name=keyword['keyword'],
                    relevance=keyword['relevance'])
            break

    page += 1
    issues_response = requests.get(issues_url, params={'state': 'all', 'page': page})
    issue_list = issues_response.json()

print("Done!")
