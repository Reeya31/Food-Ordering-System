from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','email','Phone_number','address_1','address_2','province','city','area','order_note']
        