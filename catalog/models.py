from django.db import models
from django.core.urlresolvers import reverse
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from geopy import geocoders

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


class RealEstate(models.Model):
    owner = models.ForeignKey('auth.User')
    address = models.TextField(help_text="Coloque o endereço do imóvel aqui.")
    zip_code = models.TextField(help_text="Cep vem aqui.", default = "00000-000")
    latitude = models.FloatField(default = -22.912194)
    longitude = models.FloatField(default = -43.249910)

    def __str__(self):
        return self.address

    def _calculate_coordinates(self):
        geolocator = Nominatim()
        location = geolocator.geocode(self.address)
        self.latitude = location.latitude
        self.longitude = location.longitude

    def calculate_distance(self, location):
        this_location = (self.latitude, self.longitude)
        location = (location.latitude, location.longitude)
        return vincenty(this_location, location).kilometers  

    def publish(self):
        self._calculate_coordinates()
        self.save()

    def get_absolute_url(self):
        return reverse('houses')