
from django import forms
from django.forms import DateField, ModelForm
from .models import *

class VenueForm(ModelForm):
    class Meta:
        model=Venue
        fields=['name','address','zip_code','phone','web','email_address',]
        labels={
            'name': 'Enter your Venue',
            'address': '',
            'zip_code': '',
            'phone': '',
            'web': '',
            'email_address':''
        }
        widgets= {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Venue Name'}),
            'address': forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'zip_code': forms.TextInput(attrs={'class':'form-control','placeholder':'Zip Code'}),
            'phone': forms.TextInput(attrs={'class':'form-control','placeholder':'Phone'}),
            'web': forms.TextInput(attrs={'class':'form-control','placeholder':'Web address'}),
            'email_address': forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'})
        }



class eventForm(ModelForm):
    class Meta:
        model=Event
        fields=['name','event_date','venue','description','attendees']
        Widgets={
            'event_date':forms.NumberInput(attrs={'type': 'date'})
        }