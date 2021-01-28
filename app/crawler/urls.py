from django.urls import path
from django.conf.urls import url, include
from .feedparser_test import *

urlpatterns = [
    path('parse_feed/', ParseFeed.as_view()),
    path('add_source_by_feed/', AddSourceByFeed.as_view()),
    path('crawl_source/', CrawlSource.as_view()),
    path('crawl_all_sources/', CrawlAllSources.as_view())
]
