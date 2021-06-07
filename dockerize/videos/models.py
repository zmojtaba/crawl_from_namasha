from django.db import models
from django.utils.translation import LANGUAGE_SESSION_KEY


class Category(models.Model):
    name = models.CharField(max_length=100)
    last_crawl = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Channel(models.Model):
    title = models.CharField(max_length=500, blank=True)
    link = models.CharField(max_length=1000, blank=True)
    last_crawl = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class Video(models.Model):
    title = models.CharField(max_length=500, blank=True, null=True)
    thumbnail = models.CharField(max_length=2000, blank=True, null=True)
    link = models.CharField(max_length=1000, primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    duration = models.IntegerField(null=True)
    view_count = models.IntegerField(null=True)
    publish_data = models.DateTimeField(null=True)
    last_crawl = models.DateTimeField(null=True, blank=True)


class Channel_Video(models.Model):
    title = models.CharField(max_length=500, blank=True, null=True)
    thumbnail = models.CharField(max_length=2000, blank=True, null=True)
    link = models.CharField(max_length=1000, primary_key=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    duration = models.IntegerField(null=True)
    view_count = models.IntegerField(null=True)
    publish_data = models.DateTimeField(null=True)
