import json

from django.db import models
from django.utils import timezone


class DataSet(models.Model):
    """
    Data Model for Extracted Site JSON Data
    """
    uid = models.CharField(max_length=100, null=True, unique=True)
    data = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    site = models.ForeignKey("SiteManifest", on_delete=models.DO_NOTHING, null=True)

    @property
    def to_dict(self):
        data = {
            'data': json.loads(self.data),
            'date': self.timestamp
        }
        return data

    def __str__(self):
        return "%s - %s" % (self.uid, self.site)


class SiteManifest(models.Model):
    """
    Data Model for Site Information intended for query purpose
    """
    name = models.CharField(max_length=120)
    protocol = models.CharField(max_length=10, choices=(
        ('HTTP', 'http'),
        ('HTTPS', 'https'),
        ('FTP', 'ftp'),
        ('FTPS', 'ftp')
    ), default='HTTP')
    domain = models.CharField(max_length=120)
    place_id = models.TextField()
    api_key = models.TextField()

    def __str__(self):
        return "%s - [ %s ]" % (self.name, self.domain)


class DataReport(models.Model):
    """
    Data Model for Data Difference Reporting Log
    """
    difference = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    # Serves as the bases for data comparison
    base_referer = models.ForeignKey(DataSet, on_delete=models.DO_NOTHING, related_name='base_referer')
    # Serves as the latest data for base data comparison
    data_referer = models.ForeignKey(DataSet, on_delete=models.DO_NOTHING, related_name='data_referer')

    def __str__(self):
        if self.difference != '{}':
            return "%s - [ %s ]" % (self.difference, "Some Data had been Modified")
        else:
            return "No data have been modified"
