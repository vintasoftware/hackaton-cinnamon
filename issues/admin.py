from django.contrib import admin

from .models import Issue, File, PullRequest

admin.site.register(Issue)
admin.site.register(File)
admin.site.register(PullRequest)
