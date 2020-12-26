from django import forms
from .models import Customer


#class InfoForm(forms.Form):
  #  name = forms.CharField()
   # address = forms.CharField()
    #city = forms.CharField()
    #description = forms.TextField(widget=forms.Textarea)
    #longitude = forms.FloatField()
    #latitude = forms.FloatField()
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'address', 'description', 'city', 'longitude', 'latitude',]


