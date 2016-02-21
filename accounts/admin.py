from django.contrib import admin

from accounts.models import Account, Repos

admin.site.register(Account)
admin.site.register(Repos)
