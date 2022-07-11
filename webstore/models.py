from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image

# Create your models here.
gender_choices = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other")
)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'  # For login now we will use Email insted of Username
    REQUIRED_FIELDS = ['username']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        return qs if user.is_staff else qs.filter(id=user.id)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=gender_choices, default='Female')
    email = models.EmailField(max_length=50, unique=True)
    mobile_no = PhoneNumberField(unique=True)
    avatar = models.ImageField(null=True, default="avatar.svg", upload_to='profile_picture')

    def __str__(self):
        return self.email
