from django.urls import path


from . import views

app_name = "monitor"


urlpatterns = [
    path('query', views.do_query, name="crawl")
]