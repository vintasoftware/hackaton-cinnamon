import requests

apikey = '7e01429feb1c1a6fd78aee6e1246bc25ff9dc5a5'
text = '''
Unicode QUERY_PARAM not parsed at all

In a unit test in my app I pass in the query param u'?name[]=☂' (I also tried the normally escaped u'?name[]=%E2%98%82') and the request.query_params comes back empty

Testing Django itself does not repro this error. Something about the Request wrapping done in this rest framework is failing to decode the unicode.
'''

response = requests.get(
    'http://gateway-a.watsonplatform.net/calls/text/TextGetRankedKeywords',
    params={
        'apikey': apikey,
        'text': text,
        'maxRetrieve': 10,
        'keywordExtractMode': 'strict',
        'sentiment': 0,
        'outputMode': 'json'
    })
keywords = response.json()['keywords']
print(sorted(
    [(x['text'], x['relevance']) for x in keywords],
    key=lambda t: t[1],
    reverse=True))
