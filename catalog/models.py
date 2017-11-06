from django.db import models
from django.core.urlresolvers import reverse
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
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
    zip_code = models.TextField(help_text="Cep vem aqui.", default = "00000-000")
    latitude = models.FloatField(default = -22.912194)
    longitude = models.FloatField(default = -43.249910)

    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

    def __str__(self):
        return self.address

    def _calculate_coordinates(self):
        geolocator = Nominatim()
        print("inside calculate coordinates")
        print(self.address)
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
