from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.sessions.models import Session


class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200, default=None)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class BlogData(models.Model):
    author = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    text = models.TextField()
    published_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()
