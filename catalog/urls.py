from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^houses/$', views.HouseListView.as_view(), name='houses'),
    url(r'^publish/$', views.publish_house, name='publish'),
    url(r'^houses/(?P<pk>\d+)$', views.HouseDetailView.as_view(), name='house-detail'),
    url(r'^houses/update/(?P<id>\d+)$', views.update_house, name='update-house'),
]