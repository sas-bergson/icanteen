from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm): # the form is created using django forms model
    class Meta:
        model = Order # the model to be used is defined which is the order model
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city'] # the form field is specified as in the order model