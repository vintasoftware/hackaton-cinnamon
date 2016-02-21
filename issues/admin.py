from django.contrib import admin

from .models import Issue, Tag, File, PullRequest

admin.site.register(Issue)
admin.site.register(Tag)
admin.site.register(File)
admin.site.register(PullRequest)
