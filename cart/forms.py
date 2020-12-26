from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 26)] #this will be used as a drop down for users to select quantity within the range on 1 to 26

class CartAddProductForm(forms.Form):  #this class will be used to add items to cart
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int) # here the field quantity is defined
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput) # update field is defined which will help in adding or updating of items
