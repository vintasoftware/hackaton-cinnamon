import json
import requests
from django.conf import settings

from django.template import Context, Template

from allauth.account.adapter import DefaultAccountAdapter


MESSAGE = """
Hi, I have some suggestions to help solving this issue!

The following users made pull-requests to related issues:
{% for user in users %}**{{ user }}**{% if not forloop.last %}, {% endif %}{% endfor %}

Maybe it's a good idea to assign them to this issue? Or at least ask them some tips?

Some background now. Here is a list of similar issues:
{% for issue in issues %}
{{ forloop.counter }}. [{{ issue.name }}]({{ issue.link }})
{% endfor %}
Also, these are some files that might need to change:
{% for file in files %}
{{ forloop.counter }}. [{{ file }}](https://github.com/{{user}}/{{repo}}/blob/master/{{ file }})
{% endfor %}

Hope it's useful!

Cheers,
CinnaBot."""


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
