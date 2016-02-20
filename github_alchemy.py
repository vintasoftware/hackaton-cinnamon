import requests
import gfm
from bs4 import BeautifulSoup
import re

issues_url = 'https://api.github.com/repos/kennethreitz/requests/issues'
apikey = ''

response = requests.get(issues_url)
issue_list = response.json()[:5]
issue_tag_dict = {}
for issue in issue_list:
    # remove code blocks
    issue_body = re.sub(r'```.+```', '', issue['body'], flags=re.DOTALL)

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
    keywords = response.json()['keywords']
    tags = sorted(
        [(x['text'], x['relevance']) for x in keywords],
        key=lambda t: t[1],
        reverse=True)
    issue_tag_dict[issue['number']] = {
        'issue': issue['title'],
        'text': issue['body'],
        'tags': tags
    }

import pprint
pprint.pprint(issue_tag_dict)


# print('with code\n', gfm.markdown(response_body))
# print('\n' * 10)
# soup = BeautifulSoup(gfm.markdown(response_body))
# soup
# print('without code\n', )


# apikey = '7e01429feb1c1a6fd78aee6e1246bc25ff9dc5a5'
# text = '''
# Unicode QUERY_PARAM not parsed at all

# In a unit test in my app I pass in the query param u'?name[]=☂' (I also tried the normally escaped u'?name[]=%E2%98%82') and the request.query_params comes back empty

# Testing Django itself does not repro this error. Something about the Request wrapping done in this rest framework is failing to decode the unicode.
# '''

# response = requests.get(
#     'http://gateway-a.watsonplatform.net/calls/text/TextGetRankedKeywords',
#     params={
#         'apikey': apikey,
#         'text': text,
#         'maxRetrieve': 10,
#         'keywordExtractMode': 'strict',
#         'sentiment': 0,
#         'outputMode': 'json'
#     })
# keywords = response.json()['keywords']
# print(sorted(
#     [(x['text'], x['relevance']) for x in keywords],
#     key=lambda t: t[1],
#     reverse=True))
