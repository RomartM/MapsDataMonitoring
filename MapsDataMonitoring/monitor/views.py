from django.shortcuts import render
from django.http import HttpResponse
from .models import DataSet, SiteManifest, DataReport
from jsondiff import diff
import requests
import json
from uuid import uuid4


def test(request):
    context = {
       "data1":{
   "address_components":[
      {
         "long_name":"Domingo Belez Street",
         "short_name":"Domingo Belez St",
         "types":[
            "route"
         ]
      },
      {
         "long_name":"Malaybalay City",
         "short_name":"MC",
         "types":[
            "locality",
            "political"
         ]
      },
      {
         "long_name":"Misamis Oriental",
         "short_name":"Misamis Oriental",
         "types":[
            "administrative_area_level_2",
            "political"
         ]
      },
      {
         "long_name":"Northern Mindanao",
         "short_name":"Northern Mindanao",
         "types":[
            "administrative_area_level_1",
            "political"
         ]
      },
      {
         "long_name":"Philippines",
         "short_name":"PH",
         "types":[
            "country",
            "political"
         ]
      },
      {
         "long_name":"9000",
         "short_name":"9000",
         "types":[
            "postal_code"
         ]
      }
   ],
   "adr_address":"3rd Floor, Egmedio Building, Corrales Avenue, <span class=\"street-address\">Domingo Velez St</span>, <span class=\"locality\">Cagayan de Oro</span>, <span class=\"postal-code\">9000</span> <span class=\"region\">Misamis Oriental</span>, <span class=\"country-name\">Philippines</span>",
   "formatted_address":"3rd Floor, Egmedio Building, Corrales Avenue, Domingo Velez St, Cagayan de Oro, 9000 Misamis Oriental, Philippines",
   "formatted_phone_number":"(088) 881 2729",
   "geometry":["None"],
   "icon":"https://maps.gstatic.com/mapfiles/place_api/icons/generic_business-71.png",
   "id":"0cd35cb90b52ce69538d3ffe95efd6ec56ff355f",
   "international_phone_number":[
      "+63 88 881 2729",
      "+63 88 881 2730"
   ],
   "name":"Syntactics Inc",
   "opening_hours":{
      "open_now":True,
      "periods":[
         {
            "close":{
               "day":1,
               "time":"2200"
            },
            "open":{
               "day":1,
               "time":"0600"
            }
         },
         {
            "close":{
               "day":2,
               "time":"2200"
            },
            "open":{
               "day":2,
               "time":"0600"
            }
         },
         {
            "close":{
               "day":3,
               "time":"2200"
            },
            "open":{
               "day":3,
               "time":"0600"
            }
         },
         {
            "close":{
               "day":4,
               "time":"2200"
            },
            "open":{
               "day":4,
               "time":"0600"
            }
         },
         {
            "close":{
               "day":5,
               "time":"2200"
            },
            "open":{
               "day":5,
               "time":"0600"
            }
         }
      ],
      "weekday_text":[
         "Monday: 6:00 AM \u2013 10:00 PM",
         "Tuesday: 6:00 AM \u2013 10:00 PM",
         "Wednesday: 6:00 AM \u2013 10:00 PM",
         "Thursday: 6:00 AM \u2013 10:00 PM",
         "Friday: 6:00 AM \u2013 10:00 PM",
         "Saturday: Closed",
         "Sunday: Closed"
      ]
   },
   "photos":[
      {
         "height":2592,
         "html_attributions":[
            "<a href=\"https://maps.google.com/maps/contrib/110405781852045512504/photos\">Syntactics Inc.</a>"
         ],
         "width":4608
      },
      {
         "height":4608,
         "html_attributions":[
            "<a href=\"https://maps.google.com/maps/contrib/110405781852045512504/photos\">Syntactics Inc.</a>"
         ],
         "width":2592
      },
      {
         "height":4608,
         "html_attributions":[
            "<a href=\"https://maps.google.com/maps/contrib/110405781852045512504/photos\">Syntactics Inc.</a>"
         ],
         "width":2592
      },
      {
         "height":2322,
         "html_attributions":[
            "<a href=\"https://maps.google.com/maps/contrib/110242641114174429307/photos\">Joan Merced Sheng</a>"
         ],
         "width":4128
      },
      {
         "height":2592,
         "html_attributions":[
            "<a href=\"https://maps.google.com/maps/contrib/110405781852045512504/photos\">Syntactics Inc.</a>"
         ],
         "width":4608
      },
      {
         "height":1015,
         "html_attributions":[
            "<a href=\"https://maps.google.com/maps/contrib/110405781852045512504/photos\">Syntactics Inc.</a>"
         ],
         "width":1800
      },
      {
         "height":1012,
         "html_attributions":[
            "<a href=\"https://maps.google.com/maps/contrib/110405781852045512504/photos\">Syntactics Inc.</a>"
         ],
         "width":1800
      },
      {
         "height":270,
         "html_attributions":[
            "<a href=\"https://maps.google.com/maps/contrib/110405781852045512504/photos\">Syntactics Inc.</a>"
         ],
         "width":480
      },
      {
         "height":357,
         "html_attributions":[
            "<a href=\"https://maps.google.com/maps/contrib/107055856903122416970/photos\">Wilfredo P. Kaami\u00f1o Jr.</a>"
         ],
         "width":1031
      },
      {
         "height":1015,
         "html_attributions":[
            "<a href=\"https://maps.google.com/maps/contrib/110405781852045512504/photos\">Syntactics Inc.</a>"
         ],
         "width":1800
      }
   ],
   "place_id":"ChIJZ-kb9tny_zIRYyaihWkIIN8",
   "plus_code":{
      "compound_code":"FJHW+WR Cagayan de Oro, Misamis Oriental, Philippines",
      "global_code":"6QW6FJHW+WR"
   },
   "rating":4.9,
   "reference":"ChIJZ-kb9tny_zIRYyaihWkIIN8",
   "reviews":[
      {
         "author_name":"Felipe Gonzales",
         "author_url":"https://www.google.com/maps/contrib/114318703839356112577/reviews",
         "language":"en",
         "profile_photo_url":"https://lh4.googleusercontent.com/-qN-JuGc0CI8/AAAAAAAAAAI/AAAAAAAAAW8/Yqdx5qQO-08/s128-c0x00000000-cc-rp-mo/photo.jpg",
         "rating":5,
         "relative_time_description":"10 months ago",
         "text":"Great organization and such a friendly team. When I have a overflow of tasks, Syntactics is there to help with graphic design, administrative tasks, and more. Thank you Jalou, Pamela, and Harlie.",
         "time":1518033432
      },
      {
         "author_name":"Joan Merced Sheng",
         "author_url":"https://www.google.com/maps/contrib/110242641114174429307/reviews",
         "language":"en",
         "profile_photo_url":"https://lh5.googleusercontent.com/-a-XBFqan9EM/AAAAAAAAAAI/AAAAAAAA5So/yiwCDio9jcE/s128-c0x00000000-cc-rp-mo-ba5/photo.jpg",
         "rating":5,
         "relative_time_description":"6 months ago",
         "text":"Excellent service and employees are full of enthusiasm.",
         "time":1529403588
      },
      {
         "author_name":"Perwati Nadal",
         "author_url":"https://www.google.com/maps/contrib/104380469963383888542/reviews",
         "language":"en",
         "profile_photo_url":"https://lh6.googleusercontent.com/-EWg1vGf2XnA/AAAAAAAAAAI/AAAAAAAAAAA/AKxrwcZxozljXMK0mFzfZuBpjENkY31GBw/s128-c0x00000000-cc-rp-mo/photo.jpg",
         "rating":5,
         "relative_time_description":"2 years ago",
         "text":"My experience with Syntactics for the last 2 projects so far has been a good one so far. They built 1 website for me and another one for my client and my client could not stop thanking me for the job done. I have had my experience with other BPO Companies in the Philippines that does website design and development but so far, this team has been on time and has been good in their communications with me.",
         "time":1461892801
      },
      {
         "author_name":"Infinity Foundry",
         "author_url":"https://www.google.com/maps/contrib/111866758733024550183/reviews",
         "language":"en",
         "profile_photo_url":"https://lh6.googleusercontent.com/-SWvtxrTY9eA/AAAAAAAAAAI/AAAAAAAAAcg/mU1VaacZX6k/s128-c0x00000000-cc-rp-mo/photo.jpg",
         "rating":5,
         "relative_time_description":"3 years ago",
         "text":"No task is too big, or too small. The talented team at Syntactics inc are a pleasure to work with.",
         "time":1442546107
      },
      {
         "author_name":"Alaiza Geene Maandig",
         "author_url":"https://www.google.com/maps/contrib/106854329468891418599/reviews",
         "profile_photo_url":"https://lh5.googleusercontent.com/-O84yPHl17BE/AAAAAAAAAAI/AAAAAAAAnYo/0n3JIwiI93s/s128-c0x00000000-cc-rp-mo/photo.jpg",
         "rating":4,
         "relative_time_description":"4 weeks ago",
         "text":"",
         "time":1543987099
      }
   ],
   "scope":"GOOGLE",
   "types":[
      "point_of_interest",
      "establishment"
   ],
   "url":"https://maps.google.com/?cid=16077859919019255395",
   "utc_offset":480,
   "vicinity":"3rd Floor, Egmedio Building, Corrales Avenue, Domingo Velez Street, Cagayan de Oro",
   "website":"http://www.syntacticsinc.com/"
},
       "data2":{"address_components": [{"long_name": "Domingo Velez Street", "short_name": "Domingo Velez St", "types": ["route"]}, {"long_name": "Cagayan de Oro", "short_name": "CDO", "types": ["locality", "political"]}, {"long_name": "Misamis Oriental", "short_name": "Misamis Oriental", "types": ["administrative_area_level_2", "political"]}, {"long_name": "Northern Mindanao", "short_name": "Northern Mindanao", "types": ["administrative_area_level_1", "political"]}, {"long_name": "Philippines", "short_name": "PH", "types": ["country", "political"]}, {"long_name": "9000", "short_name": "9000", "types": ["postal_code"]}], "adr_address": "3rd Floor, Egmedio Building, Corrales Avenue, <span class=\"street-address\">Domingo Velez St</span>, <span class=\"locality\">Cagayan de Oro</span>, <span class=\"postal-code\">9000</span> <span class=\"region\">Misamis Oriental</span>, <span class=\"country-name\">Philippines</span>", "formatted_address": "3rd Floor, Egmedio Building, Corrales Avenue, Domingo Velez St, Cagayan de Oro, 9000 Misamis Oriental, Philippines", "formatted_phone_number": "(088) 881 2729", "geometry": {"location": {"lat": 8.479841999999998, "lng": 124.647058}, "viewport": {"northeast": {"lat": 8.481143730291501, "lng": 124.6484829302915}, "southwest": {"lat": 8.478445769708497, "lng": 124.6457849697085}}}, "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/generic_business-71.png", "id": "0cd35cb90b52ce69538d3ffe95efd6ec56ff355f", "international_phone_number": "+63 88 881 2729", "name": "Syntactics Inc", "opening_hours": {"open_now": True, "periods": [{"close": {"day": 1, "time": "2200"}, "open": {"day": 1, "time": "0600"}}, {"close": {"day": 2, "time": "2200"}, "open": {"day": 2, "time": "0600"}}, {"close": {"day": 3, "time": "2200"}, "open": {"day": 3, "time": "0600"}}, {"close": {"day": 4, "time": "2200"}, "open": {"day": 4, "time": "0600"}}, {"close": {"day": 5, "time": "2200"}, "open": {"day": 5, "time": "0600"}}], "weekday_text": ["Monday: 6:00 AM \u2013 10:00 PM", "Tuesday: 6:00 AM \u2013 10:00 PM", "Wednesday: 6:00 AM \u2013 10:00 PM", "Thursday: 6:00 AM \u2013 10:00 PM", "Friday: 6:00 AM \u2013 10:00 PM", "Saturday: Closed", "Sunday: Closed"]}, "photos": [{"height": 2592, "html_attributions": ["<a href=\"https://maps.google.com/maps/contrib/110405781852045512504/photos\">Syntactics Inc.</a>"], "width": 4608}, {"height": 4608, "html_attributions": ["<a href=\"https://maps.google.com/maps/contrib/110405781852045512504/photos\">Syntactics Inc.</a>"], "width": 2592}, {"height": 4608, "html_attributions": ["<a href=\"https://maps.google.com/maps/contrib/110405781852045512504/photos\">Syntactics Inc.</a>"], "width": 2592}, {"height": 2322, "html_attributions": ["<a href=\"https://maps.google.com/maps/contrib/110242641114174429307/photos\">Joan Merced Sheng</a>"], "width": 4128}, {"height": 2592, "html_attributions": ["<a href=\"https://maps.google.com/maps/contrib/110405781852045512504/photos\">Syntactics Inc.</a>"], "width": 4608}, {"height": 1015, "html_attributions": ["<a href=\"https://maps.google.com/maps/contrib/110405781852045512504/photos\">Syntactics Inc.</a>"], "width": 1800}, {"height": 1012, "html_attributions": ["<a href=\"https://maps.google.com/maps/contrib/110405781852045512504/photos\">Syntactics Inc.</a>"], "width": 1800}, {"height": 270, "html_attributions": ["<a href=\"https://maps.google.com/maps/contrib/110405781852045512504/photos\">Syntactics Inc.</a>"], "width": 480}, {"height": 357, "html_attributions": ["<a href=\"https://maps.google.com/maps/contrib/107055856903122416970/photos\">Wilfredo P. Kaami\u00f1o Jr.</a>"], "width": 1031}, {"height": 1015, "html_attributions": ["<a href=\"https://maps.google.com/maps/contrib/110405781852045512504/photos\">Syntactics Inc.</a>"], "width": 1800}], "place_id": "ChIJZ-kb9tny_zIRYyaihWkIIN8", "plus_code": {"compound_code": "FJHW+WR Cagayan de Oro, Misamis Oriental, Philippines", "global_code": "6QW6FJHW+WR"}, "rating": 4.9, "reference": "ChIJZ-kb9tny_zIRYyaihWkIIN8", "reviews": [{"author_name": "Felipe Gonzales", "author_url": "https://www.google.com/maps/contrib/114318703839356112577/reviews", "language": "en", "profile_photo_url": "https://lh4.googleusercontent.com/-qN-JuGc0CI8/AAAAAAAAAAI/AAAAAAAAAW8/Yqdx5qQO-08/s128-c0x00000000-cc-rp-mo/photo.jpg", "rating": 5, "relative_time_description": "10 months ago", "text": "Great organization and such a friendly team. When I have a overflow of tasks, Syntactics is there to help with graphic design, administrative tasks, and more. Thank you Jalou, Pamela, and Harlie.", "time": 1518033432}, {"author_name": "Joan Merced Sheng", "author_url": "https://www.google.com/maps/contrib/110242641114174429307/reviews", "language": "en", "profile_photo_url": "https://lh5.googleusercontent.com/-a-XBFqan9EM/AAAAAAAAAAI/AAAAAAAA5So/yiwCDio9jcE/s128-c0x00000000-cc-rp-mo-ba5/photo.jpg", "rating": 5, "relative_time_description": "6 months ago", "text": "Excellent service and employees are full of enthusiasm.", "time": 1529403588}, {"author_name": "Perwati Nadal", "author_url": "https://www.google.com/maps/contrib/104380469963383888542/reviews", "language": "en", "profile_photo_url": "https://lh6.googleusercontent.com/-EWg1vGf2XnA/AAAAAAAAAAI/AAAAAAAAAAA/AKxrwcZxozljXMK0mFzfZuBpjENkY31GBw/s128-c0x00000000-cc-rp-mo/photo.jpg", "rating": 5, "relative_time_description": "2 years ago", "text": "My experience with Syntactics for the last 2 projects so far has been a good one so far. They built 1 website for me and another one for my client and my client could not stop thanking me for the job done. I have had my experience with other BPO Companies in the Philippines that does website design and development but so far, this team has been on time and has been good in their communications with me.", "time": 1461892801}, {"author_name": "Infinity Foundry", "author_url": "https://www.google.com/maps/contrib/111866758733024550183/reviews", "language": "en", "profile_photo_url": "https://lh6.googleusercontent.com/-SWvtxrTY9eA/AAAAAAAAAAI/AAAAAAAAAcg/mU1VaacZX6k/s128-c0x00000000-cc-rp-mo/photo.jpg", "rating": 5, "relative_time_description": "3 years ago", "text": "No task is too big, or too small. The talented team at Syntactics inc are a pleasure to work with.", "time": 1442546107}, {"author_name": "Alaiza Geene Maandig", "author_url": "https://www.google.com/maps/contrib/106854329468891418599/reviews", "profile_photo_url": "https://lh5.googleusercontent.com/-O84yPHl17BE/AAAAAAAAAAI/AAAAAAAAnYo/0n3JIwiI93s/s128-c0x00000000-cc-rp-mo/photo.jpg", "rating": 4, "relative_time_description": "4 weeks ago", "text": "", "time": 1543987099}], "scope": "GOOGLE", "types": ["point_of_interest", "establishment"], "url": "https://maps.google.com/?cid=16077859919019255395", "utc_offset": 480, "vicinity": "3rd Floor, Egmedio Building, Corrales Avenue, Domingo Velez Street, Cagayan de Oro", "website": "http://www.syntacticsinc.com/"}
    }

    return render(request, "test_layout.html", context)


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
