# Celery Dependencies
from __future__ import absolute_import, unicode_literals
from celery import task
# App Core Models
from .models import DataSet, SiteManifest, DataReport
# JSON Difference Detector
from jsondiff import diff
# Backend Email Dependencies
from django.core.mail import send_mail
from django.conf import settings
# Unique ID Generator Dependency
from uuid import uuid4
# External URL Request Dependency
import requests
# JSON Dependency
import json


@task()
def gmap_data_query():
    """
    Description: Default Task for Google Maps Places Data Monitoring Query
    """
    # Fetch all site list
    site_list = SiteManifest.objects.all()
    # Call DataSet Model Objects
    data_obj = DataSet.objects
    # DataSet List Reserves
    data_list = None
    # Verifies DataSet Model is not empty
    if data_obj.exists():
        # Sort DataSet by lates timestamp
        data_list = data_obj.latest('timestamp')
    # DataSet Entry Response Reserves
    stat = ""
    # Loop all site list
    for data in site_list:
        # Google API Place request pattern
        url = "%s://%s/maps/api/place/details/json?placeid=%s&key=%s" % \
              (str(data.protocol).lower(),
               str(data.domain).lower(),
               data.place_id,
               data.api_key)
        # Fetch JSON Data
        dict_data = requests.get(url).json()
        # Catch Error when API became busted
        try:
            # Remove unnecessary dynamic data
            [i.pop('photo_reference') for i in dict_data.get('result').get('photos')]
        except AttributeError:
            return print(str('Google Maps API Usage Error: %s' % dict_data.get('status')))
        except ConnectionError:
            return print(str('Failed Contacting Google API Servers'))
        # Create DataSet Entry
        stat = DataSet.objects.create(
            uid=str(uuid4()),
            data=json.dumps(dict_data.get('result')),
            site=SiteManifest.objects.get(pk=1)
        )
    # Executes data report logger and deploy changes detection algo
    response = data_report_logger(data_list, data_obj)
    # Print Response and DataSet ID to console
    print("DRL: %s\n DSID: %s" % (response, str(stat)))


def data_report_logger(data_list, data_obj):
    """
    Description: Create DataSet Report Entry
    :param data_list: DataSet List(QuerySet)
    :param data_obj: DataSet Objects
    """
    if data_list is not None:
        # Sort newly DataList Data
        fresh_data = data_obj.latest('timestamp')
        # Data Changes Execution
        result = diff(json.loads(data_list.data),
                      json.loads(fresh_data.data))
        result_counterpart = diff(json.loads(fresh_data.data),
                      json.loads(data_list.data))
        # Create DataReport Entry
        DataReport.objects.create(
            difference=result,
            base_referer=data_list,
            data_referer=fresh_data
        )
        # Checks whether data is modified
        print(result)
        if result != {}:
            # Send Report if some data changes detected
            email_list = []
            [email_list.append(r.email) for r in data_list.site.email_recipients.all()]
            print(email_list)
            alert_email_report(
                dict([
                    ('subject', 'Alert - Changes Detected - %s' % data_list.site.name),
                    ('message', 'After Changes: %s \n Before Changes: %s' % (result, result_counterpart)),
                    ('recipient_list', email_list)
                ])
            )
            print('Changes Detected!')
            return 'Email Sent'
        else:
            return 'No changes detected'
    else:
        return 'Data List Empty'


def alert_email_report(data_manifest):
    """
    Description: Allow to send alert emails when changes of data detected
    :param data_manifest: Dictionary type parameter which contains three keys
        [subject] - String
        [message] - String
        [recipient_list] - List
    """
    try:
        subject = data_manifest.get('subject')
        message = data_manifest.get('message')
        # See settings.py for EMAIL_HOST_USER modification
        email_from = settings.EMAIL_HOST_USER
        recipient_list = data_manifest.get('recipient_list')
        # Send Email
        send_mail(subject, message, email_from, recipient_list)
        print('Message Sent')
        # todo: more specific Error handling
    except IndexError:
        print('Something went wrong')

