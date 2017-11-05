from django import forms
from .validators import validate_address
from .models import RealEstate

class PublishHouseForm(forms.ModelForm):
    address = forms.CharField(label='Endereço', validators=[validate_address])
    zip_code = forms.CharField(label='CEP')   

    class Meta:
        model = RealEstate
        fields = ( 'image', 'address', 'zip_code') 
    

class SearchNearbyForm(forms.Form):
    CHOICES = (('5', '5 km'), ('10', '10 km'), ('20', '20 km'), ('30', '30 km'),
               ('40', '40 km'), ('50', '50 km'), ('100', '100 km'))

    address = forms.CharField(label='Endereço', validators=[validate_address])
    distance = forms.TypedChoiceField(label='Distância', choices=CHOICES, coerce=int)