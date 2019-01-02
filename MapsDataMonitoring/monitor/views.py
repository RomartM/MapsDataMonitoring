from django.shortcuts import render
from django.http import HttpResponse
from .models import DataSet, SiteManifest, DataReport
from jsondiff import diff
import requests
import json
from uuid import uuid4


def do_query(request):
    site_list = SiteManifest.objects.all()
    data_obj = DataSet.objects
    data_list = None
    if data_obj.exists():
        data_list = data_obj.latest('timestamp')
    stat = ""
    for data in site_list:
        # API request pattern
        url = "%s://%s/maps/api/place/details/json?placeid=%s&key=%s" % \
              (str(data.protocol).lower(),
               str(data.domain).lower(),
               data.place_id,
               data.api_key)
        # Fetch JSON Data
        dict_data = requests.get(url).json()
        # Catch Error when API became busted
        try:
            # Try to remove unnecessary data
            [i.pop('photo_reference') for i in dict_data.get('result').get('photos')]
        except AttributeError:
            return HttpResponse(content=str('Google Maps API Usage Error: %s' % dict_data.get('status')))
        except ConnectionError:
            return HttpResponse(content=str('Failed Contacting Google API Servers'))
        # Create and Save Data to Database
        stat = DataSet.objects.create(
            uid=str(uuid4()),
            data=json.dumps(dict_data.get('result')),
            site=SiteManifest.objects.get(pk=1)
        )
    if data_list is not None:
        fresh_data = data_obj.latest('timestamp')
        result = diff(json.loads(data_list.data),
                      json.loads(fresh_data.data))
        DataReport.objects.create(
            difference=result,
            base_referer=data_list,
            data_referer=fresh_data
        )
        return HttpResponse(content=str(result))
    return HttpResponse(content=str(stat.pk))
