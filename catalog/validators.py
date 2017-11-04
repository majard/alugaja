from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from geopy.geocoders import Nominatim


def validate_address(value):
    geolocator = Nominatim()
    location = geolocator.geocode(value)

    if (location == None):
        raise ValidationError(
            _('Não encontramos o endereço: %(value)s. Tente novamente em outro formato.'),
            params={'value': value},
        )
