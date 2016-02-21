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
apikey = '7e01429feb1c1a6fd78aee6e1246bc25ff9dc5a5'
repo_owner = 'evansd'
repo = 'whitenoise'

page = 1
issues_response = requests.get(issues_url, params={'state': 'all', 'page': page})
issue_list = issues_response.json()
while issue_list:
    print('Page', page)
    for gh_issue in issue_list:
        print('Processing', gh_issue['number'])
        issue = Issue.objects.create(
            number=gh_issue['number'],
            title=gh_issue['title'],
            body=gh_issue['body'] or '',
            repo_owner=repo_owner,
            repo=repo,
            raw=str(gh_issue))

        # add title and remove code blocks
        issue_body = issue.title + ' ' + \
            re.sub(r'```.+```', '', issue.body, flags=re.DOTALL)

        # get tags
        # try:
        #     response = requests.post(
        #         'http://gateway-a.watsonplatform.net/calls/text/TextGetRankedKeywords',
        #         params={
        #             'apikey': apikey,
        #             'text': issue_body,
        #             'maxRetrieve': 10,
        #             'keywordExtractMode': 'strict',
        #             'sentiment': 0,
        #             'outputMode': 'json'
        #         })
        # except Exception:
        #     print('Watson error!')
        #     import traceback
        #     traceback.print_exc()
        #     print(response.text)
        # response_json = response.json()
        # if 'keywords' not in response_json:
        #     print("Failed getting tags for", issue.number)
        #     print("Got:")
        #     print(response_json)
        # keyword_list = response_json['keywords']

        # for keyword in keyword_list:
        #     Tag.objects.create(
        #         issue=issue,
        #         name=keyword['text'],
        #         relevance=keyword['relevance'])

        keyword_list = textrank.extract_keywords(issue_body)
        for name, relevance in keyword_list:
            Tag.objects.create(
                issue=issue,
                name=name,
                relevance=relevance)

    page += 1
    issues_response = requests.get(issues_url, params={'state': 'all', 'page': page})
    issue_list = issues_response.json()

print("Done!")
