from django.db import models
from django.utils import timezone
# Create your models here.

class Sources(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=100, default='')
    link = models.CharField(max_length=1000, default='')
    rss = models.CharField(max_length=1000, default='')
    avatar = models.CharField(max_length=1000, default='')

    class Meta:
        db_table = "sources"

class Entries(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length=1000, default='')
    link = models.CharField(max_length=1000, default='')
    description = models.CharField(max_length=1000, default='')
    content = models.TextField(default='')

    pub_date = models.DateTimeField(default=timezone.now)
    crawl_date = models.DateTimeField(default=timezone.now)

    source_id = models.ForeignKey(Sources, on_delete=models.CASCADE)
    source_name = models.CharField(max_length=100, default='')

    class Meta:
        db_table = "entries"

