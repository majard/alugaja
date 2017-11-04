from django import forms
from .validators import validate_address
    
class PublishHouseForm(forms.Form):
    address = forms.CharField(label='Endereço', validators=[validate_address])
    zip_code = forms.CharField(label='CEP')