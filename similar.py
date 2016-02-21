import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.local")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from issues.models import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

issue_number = 21
issue = Issue.objects.get(number=issue_number)
issue_and_data = sorted([(obj.number, obj.get_feature())
                         for obj in Issue.objects.order_by('number')])
issue_number_to_index = {x[0]: i for i, x in enumerate(issue_and_data)}
index_to_issue_number = {i: x[0] for i, x in enumerate(issue_and_data)}
tfidf = TfidfVectorizer().fit_transform([x[1] for x in issue_and_data])
cosine_similarities = linear_kernel(
    tfidf[issue_number_to_index[issue_number]:issue_number_to_index[issue_number] + 1], tfidf).flatten()
related_docs_indices = cosine_similarities.argsort()[:-5:-1]

print("For issue {}".format(issue))
print("similar ones are:")
for index in related_docs_indices:
    similar = Issue.objects.get(number=index_to_issue_number[index])
    print(similar)

# for issue in Issue.objects.order_by('created'):
#     print(issue.title, issue.body.replace('\n', '').replace('\r', ''))

# for issue in Issue.objects.order_by('created'):
#     print(issue.pk)

# similarity
# for issue in Issue.objects.all():
#     other_issues = Issue.objects.exclude(pk=issue.pk)


# # split tags
# for tag in Tag.objects.all():
#     names = tag.name.split()
#     if len(names) > 1:
#         print('Will split:', tag.name)
#         tag.name = names[0]
#         for name in names[1:]:
#             Tag.objects.create(
#                 issue=tag.issue,
#                 name=name,
#                 relevance=tag.relevance)
#         tag.save()
