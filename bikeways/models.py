from __future__ import unicode_literals

from django.db import models


class BikewayCategory(models.Model):
    name = models.CharField(max_length=255)
    is_separated = models.BooleanField()

    def __unicode__(self):
        return self.name


class Bikeway(models.Model):
    CONDITION_CHOICES = [
        ('bad', "Bad"),
        ('regular', "Regular"),
        ('good', "Good")]

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    condition = models.CharField(max_length=255,
                                 choices=CONDITION_CHOICES)
    category = models.ForeignKey(BikewayCategory, related_name='bikeways')
    length = models.PositiveIntegerField()

    def __unicode__(self):
        return "{} - {}".format(self.name, self.location)
