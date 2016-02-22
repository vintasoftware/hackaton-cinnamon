import json
import requests
from django.conf import settings

from django.template import Context, Template

from allauth.account.adapter import DefaultAccountAdapter


MESSAGE = """
Here is our recommendation for the assignment ordinated by performance and availability:
{% for user in users %}
{{ forloop.counter }}. @{{ user }}
{% endfor %}
Assign the issue to someone. After this step we'll send more informations to help the coder.

We've a few suggestions to helps you to solve this issue!
Here are a list with similar issues:
{% for issue in issues %}
{{ forloop.counter }}. [{{ issue.name }}]({{ issue.link }})
{% endfor %}
Possible files where you'll need to work:
{% for file in files %}
{{ forloop.counter }}. [{{ file }}](https://github.com/{{user}}/{{repo}}/blob/master/{{ file }})
{% endfor %}

We hope have helped!
Thanks,

Cinnabot."""


class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        return '/repo/list/'


def comment_on_issue(user, repo, issue, users, issues, files):
    url = 'https://api.github.com/repos/{}/{}/issues/{}/comments'.format(user, repo, issue)
    headers = {'Authorization': 'token {}'.format(settings.CINNABOT_TOKEN)}

    template = Template(MESSAGE)
    c = Context({'users': users, 'issues': issues, 'files': files,
                 'user': user, 'repo': repo})
    message = template.render(c)

    data = json.dumps({'body': message})
    return requests.post(url, data=data, headers=headers)
