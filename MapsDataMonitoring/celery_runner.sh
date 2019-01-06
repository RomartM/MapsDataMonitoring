#!/bin/sh
celery -A MapsDataMonitoring beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler &
celery -A MapsDataMonitoring worker -l info &
tail -f /dev/null