from django import forms
from .validators import validate_address
    
class PublishHouseForm(forms.Form):
    address = forms.CharField(label='Endereço', validators=[validate_address])
    zip_code = forms.CharField(label='CEP')

class SearchNearbyForm(forms.Form):
    CHOICES = (('10', '10'), ('20', '20'), ('30', '30'),
               ('40', '40'), ('50', '50'), ('100', '100'))

    address = forms.CharField(label='Endereço', validators=[validate_address])
    distance = forms.TypedChoiceField(choices=CHOICES, coerce=int)