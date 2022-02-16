from unittest.util import _MAX_LENGTH
from django.db import models
from rest_framework import serializers



# Create your models here.


# class NewsItem(serializers.Serializer):
#     title = serializers.CharField()
#     description = serializers.CharField()
#     link = serializers.URLField()
#     guid = serializers.CharField(max_length=200)
#     pubDate = serializers.DateTimeField()

#     escription
# link
# guid
# pubDate

class NewsItem(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=200)
    link = serializers.URLField()


class IEEEListSerializer(NewsItem):
    pubDate = serializers.CharField(max_length=200)
    guid = serializers.CharField(max_length=200)
    creator = serializers.CharField(max_length=200)


class ARSTechnicaListSerializer(NewsItem):
    pass


class HowToGeekListSerializer(NewsItem):
    pubDate = serializers.CharField(max_length=200)
    creator = serializers.CharField(max_length=200)
    guid = serializers.CharField(max_length=200)


class BBCListSerializer(NewsItem):
    pubDate = serializers.CharField(max_length=200)
    guid = serializers.CharField(max_length=200)


class TechCrunchListSerializer(NewsItem):
    pubDate = serializers.CharField(max_length=200)
    guid = serializers.CharField(max_length=200)


class MITListSerializer(NewsItem):
    content = serializers.CharField(max_length=4000)
    pubDate = serializers.CharField(max_length=200)


class WiredListSerializer(NewsItem):
    image = serializers.URLField()
    guid = serializers.CharField(max_length=200)
    pubDate = serializers.CharField(max_length =200)
    creator = serializers.CharField(max_length=200)


class HackerNewsListSerializer(NewsItem):
    comments = serializers.CharField(max_length=200)
    # creator = serializers.CharField(max_length=200)
    guid = serializers.CharField(max_length=200)
    pubDate = serializers.CharField()


class TechMemeListSerializer(NewsItem):
    pubDate = serializers.CharField(max_length=200)
    guid = serializers.CharField(max_length=200)


class ReuterListSerializer(NewsItem):
    pubDate = serializers.CharField(max_length=200)
    guid = serializers.CharField(max_length=200)

class NYTListSerializer(NewsItem):
    creator = serializers.CharField(max_length=200)
    guid = serializers.CharField(max_length=200)
    pubDate = serializers.DateTimeField()
    image = serializers.UUIDField()


class CNNListSerializer(NewsItem):
    guid = serializers.CharField(max_length=200)
    pubDate = serializers.DateTimeField()
    image = serializers.URLField()


