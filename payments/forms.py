from django import forms


class PaymentForm(forms.Form):
    name = forms.CharField(label='Names')

class SubmitForm(forms.Form):
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name')
    cost= forms.DecimalField(max_digits=10, decimal_places=2)
    total_price = forms.IntegerField(localize=True)
    tel = forms.IntegerField(label='Tel',help_text='Number used for payment')
    email = forms.EmailField(label='Email')
    order_date = forms.DateField(label = 'Order Date')
    delivery_date = forms.DateField(label = 'Delivery Date')
