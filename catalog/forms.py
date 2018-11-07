from django import forms
from .validators import validate_address
from django.core.validators import MinValueValidator
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
               
    BEDROOM_CHOICES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4+'))

    ORDERING_CHOICES = (('Distance', 'Distância'), ('rent_price', 'Preço'), 
                        ('area', 'Área'), ('number_of_bedrooms', 'Quartos'))

    address = forms.CharField(label='Endereço', validators=[validate_address])
    distance = forms.TypedChoiceField(label='Distância', required = False, 
                                    choices=CHOICES, coerce=int, initial=DISTANCE)
    
    rent_price = forms.DecimalField(label='Preço Máximo', decimal_places=2, max_digits=10, 
                                    initial=0, required = False, validators = [MinValueValidator(0.0)])

    number_of_bedrooms = forms.TypedChoiceField(label='Mínimo de quartos', required = False, 
                                    choices=BEDROOM_CHOICES, coerce=int, initial=0)

    area = forms.IntegerField(label='Área Mínima', initial=0, 
                                required = False, validators = [MinValueValidator(0)])

    order_by = forms.TypedChoiceField(label='Ordenar por', required = False, 
                                    choices=ORDERING_CHOICES, initial=0)
                                

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