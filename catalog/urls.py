from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^houses/$', views.HouseListView.as_view(), name='houses'),
    url(r'^publish/$', views.publish_house, name='publish'),
]