from django.conf.urls import url
from . import views

app_name = "store"
urlpatterns = [
    url(r'^$', views.listing, name="listing"),
    url(r'^album/(?P<album_id>[0-9]+)/$', views.detail, name="detail"),
    url(r'^search/$', views.search, name="search")
]