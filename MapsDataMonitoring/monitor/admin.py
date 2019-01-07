from django.contrib import admin
from .models import DataSet, SiteManifest, DataReport, EmailList
import sys
from . import mod_celery_admin

sys.modules["django_celery_beat.admin"] = mod_celery_admin


# Alter Django default admin name
admin.site.site_header = 'Maps Data Monitoring Administration'
admin.site.site_title = 'Maps Data Monitoring Site Panel'


# Add Data Set Model to Django Admin
@admin.register(DataSet)
class DataSetAdmin(admin.ModelAdmin):
    pass


# Add Site Manifest Model to Django Admin
@admin.register(SiteManifest)
class SiteManifestAdmin(admin.ModelAdmin):
    pass


# Add Site Manifest Model to Django Admin
@admin.register(DataReport)
class DataReportAdmin(admin.ModelAdmin):
    pass


# Add Email List Model to Django Admin
@admin.register(EmailList)
class EmailListAdmin(admin.ModelAdmin):
    pass
