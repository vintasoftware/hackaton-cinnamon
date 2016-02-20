import requests
import re

prs_url = 'https://api.github.com/repos/kennethreitz/requests/pulls'

response = requests.get(prs_url)
pr_list = response.json()
pr_issue_dict = {}
for pr in pr_list:
    pr_body = pr['body']
    issue_numbers = re.findall(r'#\d+', pr_body)
    if len(issue_numbers) == 0:
        continue
    pr_issue_dict[pr['number']] = {
        'pr': pr['title'],
        'text': pr['body'],
        'issue_numbers': [i[1:] for i in issue_numbers]
    }

import pprint
pprint.pprint(pr_issue_dict)
