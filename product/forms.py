from django.forms import  ModelForm
from .models import Order,Invoice

class confirm_order_form(ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'payment_method']