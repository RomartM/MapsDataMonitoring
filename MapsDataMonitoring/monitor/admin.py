from django.contrib import admin
from .models import DataSet, SiteManifest, DataReport, EmailList


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
