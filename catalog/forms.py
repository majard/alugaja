from django import forms
from .validators import validate_address
from .models import RealEstate, Profile

from django.db import models

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
from alugaja.settings import DISTANCE

class PublishHouseForm(forms.ModelForm):
    address = forms.CharField(label='Endereço', validators=[validate_address])
    zip_code = forms.CharField(label='CEP')   

    class Meta:
        model = RealEstate
        fields = ( 'image', 'address', 'zip_code', 'rent_price', 'number_of_bedrooms', 'area') 
    

class SearchNearbyForm(forms.Form):
    CHOICES = (('5', '5 km'), ('10', '10 km'), ('20', '20 km'), ('30', '30 km'),
               ('40', '40 km'), ('50', '50 km'), ('100', '100 km'))

    address = forms.CharField(label='Endereço', validators=[validate_address], )
    distance = forms.TypedChoiceField(label='Distância', choices=CHOICES, coerce=int, initial=DISTANCE)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('contact',)

class SignUpForm(UserCreationForm):
    contact = models.TextField(max_length=100, blank=True)

    class Meta:
        model = User
        fields = ('username',  'password1', 'password2', )