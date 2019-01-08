from celery import current_app
from django.conf import settings
from django.contrib import admin
from django.db.models import When, Value, Case
from django.template.defaultfilters import pluralize
from django.utils.translation import ugettext_lazy as _
from django_celery_beat.admin import PeriodicTaskForm, PeriodicTask
from django_celery_beat.utils import is_database_scheduler
from kombu.utils.json import loads

from .models import DataSet, SiteManifest, DataReport, EmailList, SchedulePeriodicTask

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text  # noqa

# Alter Django default admin name
admin.site.site_header = 'Maps Data Monitoring Administration'
admin.site.site_title = 'Maps Data Monitoring Site Panel'

# Remove defualt Django Celery Periodic task
admin.site.unregister(PeriodicTask)


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


# Add Custom Periodic Task to Django Admin
@admin.register(SchedulePeriodicTask)
class CustomPeriodicTaskAdmin(admin.ModelAdmin):
    """Admin-interface for periodic tasks."""

    form = PeriodicTaskForm
    model = SchedulePeriodicTask
    celery_app = current_app
    list_display = ('__str__', 'enabled', 'interval', 'start_time', 'one_off')
    actions = ('enable_tasks', 'disable_tasks', 'toggle_tasks', 'run_tasks')
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'site', 'regtask', 'task', 'enabled', 'description', ),
            'classes': ('extrapretty', 'wide'),
        }),
        ('Schedule', {
            'fields': ('interval', 'crontab', 'solar',
                       'start_time', 'one_off'),
            'classes': ('extrapretty', 'wide'),
        }),
        ('Execution Options', {
            'fields': ('expires', 'queue', 'exchange', 'routing_key'),
            'classes': ('extrapretty', 'wide', 'collapse', 'in'),
        }),
    )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        scheduler = getattr(settings, 'CELERY_BEAT_SCHEDULER', None)
        extra_context['wrong_scheduler'] = not is_database_scheduler(scheduler)
        return super(CustomPeriodicTaskAdmin, self).changelist_view(
            request, extra_context)

    def get_queryset(self, request):
        qs = super(CustomPeriodicTaskAdmin, self).get_queryset(request)
        return qs.select_related('interval', 'crontab', 'solar')

    def _message_user_about_update(self, request, rows_updated, verb):
        """Send message about action to user.

        `verb` should shortly describe what have changed (e.g. 'enabled').

        """
        self.message_user(
            request,
            _('{0} task{1} {2} successfully {3}').format(
                rows_updated,
                pluralize(rows_updated),
                pluralize(rows_updated, _('was,were')),
                verb,
            ),
        )

    def enable_tasks(self, request, queryset):
        rows_updated = queryset.update(enabled=True)
        SchedulePeriodicTask.update_changed()
        self._message_user_about_update(request, rows_updated, 'enabled')
    enable_tasks.short_description = _('Enable selected tasks')

    def disable_tasks(self, request, queryset):
        rows_updated = queryset.update(enabled=False)
        SchedulePeriodicTask.update_changed()
        self._message_user_about_update(request, rows_updated, 'disabled')
    disable_tasks.short_description = _('Disable selected tasks')

    def _toggle_tasks_activity(self, queryset):
        return queryset.update(enabled=Case(
            When(enabled=True, then=Value(False)),
            default=Value(True),
        ))

    def toggle_tasks(self, request, queryset):
        rows_updated = self._toggle_tasks_activity(queryset)
        SchedulePeriodicTask.update_changed()
        self._message_user_about_update(request, rows_updated, 'toggled')
    toggle_tasks.short_description = _('Toggle activity of selected tasks')

    def run_tasks(self, request, queryset):
        self.celery_app.loader.import_default_modules()
        tasks = [(self.celery_app.tasks.get(task.task),
                  loads(task.args),
                  loads(task.kwargs))
                 for task in queryset]
        task_ids = [task.delay(*args, **kwargs)
                    for task, args, kwargs in tasks]
        tasks_run = len(task_ids)
        self.message_user(
            request,
            _('{0} task{1} {2} successfully run').format(
                tasks_run,
                pluralize(tasks_run),
                pluralize(tasks_run, _('was,were')),
            ),
        )
    run_tasks.short_description = _('Run selected tasks')
