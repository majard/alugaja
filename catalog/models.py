from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.core.urlresolvers import reverse
from geopy.geocoders import Nominatim
from django.contrib.gis.db.models.functions import Distance
from geopy import geocoders

from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.safestring import mark_safe

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.owner.id, filename)

class RealEstate(models.Model):
    owner = models.ForeignKey('auth.User')
    address = models.TextField(help_text="Coloque o endereço do imóvel aqui.")
    zip_code = models.TextField(help_text="Cep vem aqui.")
    location = models.PointField(geography = True)

    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

    def __str__(self):
        return self.address

    def _calculate_coordinates(self):
        geolocator = Nominatim()
        location = geolocator.geocode(self.address)
        self.location = Point(location.longitude, location.latitude)

    def calculate_distance(self, location):
        this_location = self.location
        loc = Point(location.longitude, location.latitude, srid=4326)
        dist = this_location.distance(loc) * 100
        return dist

    def publish(self):
        self._calculate_coordinates()
        self.save()

    def get_absolute_url(self):
        return reverse('house-detail', args=[str(self.id)])

    def get_update_url(self):
        return reverse('update-house', args=[str(self.id)])

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="150" height="150" />' % (self.image))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.TextField(max_length=100, blank=True)

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.id)])

    def get_update_url(self):
        return reverse('update-profile', args=[str(self.user.pk)])

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    Profile.objects.get_or_create(user=instance)
    instance.profile.save()
