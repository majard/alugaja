from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^houses/$', views.view_houses, name='houses'),
    url(r'^publish/$', views.publish_house, name='publish'),
    url(r'^houses/(?P<pk>\d+)$', views.HouseDetailView.as_view(), name='house-detail'),
    url(r'^houses/update/(?P<id>\d+)$', views.update_house, name='update-house'),
    url(r'^profiles/update/(?P<pk>\d+)$', views.update_profile, name='update-profile'),
    url(r'^profiles/(?P<pk>\d+)$', views.profile, name='profile'),
]