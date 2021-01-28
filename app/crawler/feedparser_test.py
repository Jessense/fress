import string
import json
from datetime import datetime, timedelta
from time import mktime

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import feedparser

from app.models import Sources, Entries
from .utils import crawl_entries_by_source, crawl_all_sources

class ParseFeed(APIView):
    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        rss = body['rss']
        d = feedparser.parse(rss)
        return Response({
            'feed': d['feed'],
            'entries[0]': d['entries'][0],
        })


class AddSourceByFeed(APIView):
    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        rss = body['rss']
        d = feedparser.parse(rss)
        feed = d['feed']
        source, created = Sources.objects.get_or_create(rss=rss)
        source.name = feed['title']
        source.link = feed['link']
        source.save()
        return Response({
            'msg': '已添加' + source.name,
            'source_id': source.id
        })

class CrawlSource(APIView):
    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        source_id = body['source_id']
        crawl_entries_by_source(source_id)
        return Response()


class CrawlAllSources(APIView):
    def post(self, request):
        crawl_all_sources()
        return Response()

