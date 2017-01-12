from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30)
    link = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

