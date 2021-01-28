from datetime import datetime, timedelta
from time import mktime
from django.utils import timezone
import feedparser

from app.models import Sources, Entries


def crawl_all_sources():
    sources = Sources.objects.all()
    for source in sources:
        crawl_entries_by_source(source.id)

def crawl_entries_by_source(source_id):
    source = Sources.objects.get(id=source_id)
    rss = source.rss
    d = feedparser.parse(rss)
    items = d['entries']
    for item in items:
        try:
            entry = Entries.objects.get(source_id=source, link=item['link'])
        except Entries.DoesNotExist:
            entry = Entries()
            entry.title = item['title']
            entry.link = item['link']
            entry.source_id = source
            entry.source_name = source.name
            entry.crawl_date = timezone.now()

            if 'published_parsed' in item:
                try:
                    entry.pub_date = datetime.fromtimestamp(
                        mktime(item['published_parsed']))
                except Exception as e:
                    entry.pub_date = entry.crawl_date
                    print(
                        'Exception when published_parsed: {}'.format(e))
            else:
                entry.pub_date = entry.crawl_date

            if 'summary' in item:
                entry.description = item['summary'][0:1000]

            if 'content' in item:
                entry.content = item['content'][0]['value']
            if entry.content == '' and 'summary' in item and len(item['summary']) > 0:
                entry.content = item['summary']

            entry.save()
            print(entry.link + ' - ' + entry.title)
        except Exception as e:
            print(e)
