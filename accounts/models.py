from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, is_staff, is_superuser, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(
            username=username,
            is_staff=is_staff, is_active=True,
            is_superuser=is_superuser,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True, True,
                                 **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __unicode__(self):
        return self.username


class Repos(models.Model):
    user = models.ForeignKey('accounts.Account', related_name='repositories')
    owner = models.CharField(max_length=255)
    name = models.CharField(max_length=50)
    parent_repo_owner = models.CharField(max_length=255, blank=True)
    parent_repo = models.CharField(max_length=255, blank=True)
    is_done = models.BooleanField(default=False)
    html_url = models.URLField()
