from django import forms
    
class PublishHouseForm(forms.Form):
    address = forms.CharField(help_text="Endereço: ")