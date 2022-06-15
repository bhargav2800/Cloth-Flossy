from django.forms import  ModelForm
from .models import Customer, User
from django.contrib.auth.forms import UserCreationForm
from product.models import Brand

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class MyUserUpdateForm_customer(ModelForm):
    class Meta:
        model = Customer
        fields = ['name','age','gender','mobile_no']

class UserProfile_Form(ModelForm):
    class Meta:
        model = Customer
        fields = ['email','name','age','gender','mobile_no','avatar']


class MyBrandUpdateForm_Brand(ModelForm):
    class Meta:
        model = Brand
        fields = ['brand_name']
