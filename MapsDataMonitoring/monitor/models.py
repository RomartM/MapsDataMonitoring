import json

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_celery_beat.models import PeriodicTask


class SchedulePeriodicTask(PeriodicTask):
    """
    Inherit Celery Periodic Task with custom fields
    """
    site = models.ForeignKey("SiteManifest", on_delete=models.CASCADE,
                             verbose_name=_('site'),
                             help_text=_('Place/ Establishment to schedule'))

    def save(self, *args, **kwargs):
        self.exchange = self.exchange or None
        self.routing_key = self.routing_key or None
        self.queue = self.queue or None
        self.args = "[\"%s\"]" % str(self.site.pk)
        if not self.enabled:
            self.last_run_at = None
        super(PeriodicTask, self).save(*args, **kwargs)


class DataSet(models.Model):
    """
    Data Model for Extracted Site JSON Data
    """
    uid = models.CharField(max_length=100, null=True, unique=True, help_text="Unique ID")
    data = models.TextField(help_text="JSON Data")
    timestamp = models.DateTimeField(default=timezone.now, help_text="Date created")
    site = models.ForeignKey("SiteManifest", on_delete=models.DO_NOTHING, null=True, help_text="Site referrer")

    @property
    def to_dict(self):
        data = {
            'data': json.loads(self.data),
            'date': self.timestamp
        }
        return data

    def __str__(self):
        return "%s - %s" % (self.uid, self.site)


class EmailList(models.Model):
    name = models.CharField(max_length=60, help_text="Email brief info")
    email = models.EmailField(help_text="Email Address")

    def __str__(self):
        return "[%s] - %s" % (self.email, self.name)


class SiteManifest(models.Model):
    """
    Data Model for Site Information intended for query purpose
    """
    name = models.CharField(max_length=120)
    email_recipients = models.ManyToManyField(EmailList, help_text="List of emails for site data changes alert")
    protocol = models.CharField(max_length=10, choices=(
        ('HTTP', 'http'),
        ('HTTPS', 'https'),
        ('FTP', 'ftp'),
        ('FTPS', 'ftp')
    ), default='HTTP')
    domain = models.CharField(max_length=120, help_text="Google API Domain")
    place_id = models.TextField(help_text="Google Maps Place ID")
    api_key = models.TextField(help_text="Google Maps Places API Key")

    def __str__(self):
        return "%s - [ %s ]" % (self.name, self.domain)


class DataReport(models.Model):
    """
    Data Model for Data Difference Reporting Log
    """
    difference = models.TextField(help_text="Data Changed")
    timestamp = models.DateTimeField(default=timezone.now, help_text="Time Created")
    # Serves as the bases for data comparison
    base_referer = models.ForeignKey(DataSet, on_delete=models.DO_NOTHING, related_name='base_referer',
                                     help_text="Basis of the comparison")
    # Serves as the latest data for base data comparison
    data_referer = models.ForeignKey(DataSet, on_delete=models.DO_NOTHING, related_name='data_referer',
                                     help_text="Against Basis of the comparison")

    def __str__(self):
        if self.difference != '{}':
            return "%s - [ %s ]" % (self.difference, "Some Data had been Modified")
        else:
            return "No data have been modified"

