from django.db import models

from core.models import IndexedTimeStampedModel


class Issue(IndexedTimeStampedModel):
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    body = models.TextField()
    repo_owner = models.CharField(max_length=255)
    repo = models.CharField(max_length=255)
    raw = models.TextField()

    def __unicode__(self):
        return "#{} - {}".format(self.number, self.title)


class Tag(IndexedTimeStampedModel):
    issue = models.ForeignKey(Issue, related_name='tags')
    name = models.CharField(max_length=255)
    relevance = models.FloatField()

    def __unicode__(self):
        return "{} ({})".format(self.name, self.relevance)


class File(IndexedTimeStampedModel):
    filename = models.CharField(max_length=4096)

    def __unicode__(self):
        return self.filename


class PullRequest(IndexedTimeStampedModel):
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    body = models.TextField()
    repo_owner = models.CharField(max_length=255)
    repo = models.CharField(max_length=255)
    issues = models.ManyToManyField(Issue, related_name='prs')
    files = models.ManyToManyField(File, related_name='prs')
    raw = models.TextField()

    def __unicode__(self):
        return "PR #{} - {}".format(self.number, self.title)
