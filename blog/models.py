from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200, default=None)

    def __str__(self):
        return self.username

class BlogDetails(models.Model):
    author =