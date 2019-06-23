from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^listing/$', views.listing),
    url(r'^album/(?P<album_id>[0-9]+)/$', views.detail),
    url(r'^search/$', views.search)
]