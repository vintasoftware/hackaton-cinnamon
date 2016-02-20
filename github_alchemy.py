import requests
import gfm
from bs4 import BeautifulSoup
import re

issues_url = 'https://api.github.com/repos/kennethreitz/requests/issues'

response = requests.get(issues_url)
response_body = response.json()
# assert '```' in response_body
# print('before\n', response_body)

# print('\n'*10)
# print('\n\n\nafter\n', re.sub(r'```.+```', '', response_body, flags=re.DOTALL))
re.sub(r'```.+```', '', response_body, flags=re.DOTALL)

# print('with code\n', gfm.markdown(response_body))
# print('\n' * 10)
# soup = BeautifulSoup(gfm.markdown(response_body))
# soup
# print('without code\n', )


# apikey = ''
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
