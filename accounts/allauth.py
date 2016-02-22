import json
import requests
from django.conf import settings

from django.template import Context, Template

from allauth.account.adapter import DefaultAccountAdapter


MESSAGE_1 = """
Here is our recommendation for the assignment ordinated by performance and availability:
{% for user in users %}
{{ forloop.counter }}. @{{ user }}
{% endfor %}
Assign the issue to someone. After this step we'll send more informations to help the coder.
Thanks,

Cinnabot"""

MESSAGE_2 = """
Hi @{{ developer }},
we've a few suggestions to helps you to solve this issue!
Here are a list with similar issues:
{% for issue in issues %}
{{ forloop.counter }}. #{{ issue }}
{% endfor %}
Possible files where you'll need to work:
{% for file in files %}
{{ forloop.counter }}. {{ file }}
{% endfor %}
We hope have helped!
Thanks,

Cinnabot."""


class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        return '/repo/list/'


def comment_on_issue(user, repo, issue, msg_num, users=[], developer=None, issues=[], files=[]):
    url = 'https://api.github.com/repos/{}/{}/issues/{}/comments'.format(user, repo, issue)
    headers = {'Authorization': 'token {}'.format(settings.CINNABOT_TOKEN)}

    if msg_num == 1:
        template = Template(MESSAGE_1)
        c = Context({'users': users})
    elif msg_num == 2:
        template = Template(MESSAGE_2)
        c = Context({'developer': developer, 'issues': issues, 'files': files})
    else:
        return 'message num > 2'
    message = template.render(c)

    data = json.dumps({'body': message})
    return requests.post(url, data=data, headers=headers)
