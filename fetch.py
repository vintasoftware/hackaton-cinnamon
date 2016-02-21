import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.local")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import requests
import re
from issues.models import *

issues_url = 'https://api.github.com/repos/kennethreitz/requests/issues'
apikey = '7e01429feb1c1a6fd78aee6e1246bc25ff9dc5a5'
repo_owner = 'kennethreitz'
repo = 'issues'

response = requests.get(issues_url)
issue_list = response.json()
for gh_issue in issue_list:
    print('Fetching', gh_issue['number'])
    issue = Issue.objects.create(
        number=gh_issue['number'],
        title=gh_issue['title'],
        body=gh_issue['body'],
        repo_owner=repo_owner,
        repo=repo,
        raw=str(gh_issue))

    # add title and remove code blocks
    issue_body = gh_issue['title'] + ' ' + \
        re.sub(r'```.+```', '', gh_issue['body'], flags=re.DOTALL)

    # get tags
    response = requests.get(
        'http://gateway-a.watsonplatform.net/calls/text/TextGetRankedKeywords',
        params={
            'apikey': apikey,
            'text': issue_body,
            'maxRetrieve': 10,
            'keywordExtractMode': 'strict',
            'sentiment': 0,
            'outputMode': 'json'
        })
    response_json = response.json()
    if 'keywords' not in response_json:
        print("Failed", gh_issue['number'])
        print("Got:")
        print(response_json)
    keyword_list = response_json['keywords']

    for keyword in keyword_list:
        Tag.objects.create(
            issue=issue,
            name=keyword['text'],
            relevance=keyword['relevance'])

print("Done!")
