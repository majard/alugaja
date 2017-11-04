from django.db import models
from django.core.urlresolvers import reverse
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from geopy import geocoders


class RealEstate(models.Model):
    owner = models.ForeignKey('auth.User', null = True)
    address = models.TextField(help_text="Coloque o endereço do imóvel aqui.")
    latitude = models.FloatField(default = -22.912194)
    longitude = models.FloatField(default = -43.249910)

    def __str__(self):
        return self.address

    def _calculate_lat(self):
        geolocator = Nominatim()
        location = geolocator.geocode(self.address)
        return location.latitude

    def _calculate_long(self):
        geolocator = Nominatim()
        location = geolocator.geocode(self.address)
        return location.longitude

    def _calculate_distance(self, location):
        this_location = (self.latitude, self.longitude)
        return vincenty(this_location, location).kilometers     


    def publish(self):
        latitude = self._calculate_lat()
        longitude = self._calculate_long()
        self.save()

    def get_absolute_url(self):
        return reverse('houses')