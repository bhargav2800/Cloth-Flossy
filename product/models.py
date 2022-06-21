from django.db import models
from webstore.models import User, Customer

size_choices = (
    ("XS", "XS"),
    ("S", "S"),
    ("M", "M"),
    ("L", "L"),
    ("XL", "XL"),
    ("XXL", "XXL"),
)

payment_choices = (
    ("Cash On Delivery", "Cash On Delivery"),
    ("UPI", "UPI"),
    ("Debit Card", "Debit Card"),
    ("Credit Card", "Credit Card")
)

gender_choice = (
    ("Men", "Men"),
    ("Women", "Women"),
    ("Kids", "Kids"))


# Create your models here.
class Brand(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=50, unique=True)

    def __str__(self):
        return self.brand_name

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    available_quantity = models.IntegerField()
    name = models.CharField(max_length=50)
    price = models.FloatField()
    image = models.ImageField()
    discount = models.IntegerField()
    description = models.TextField()
    no_of_purchases = models.IntegerField()
    product_size = models.CharField(max_length=10, choices=size_choices, default='XS')
    Target_audience = models.CharField(max_length=10, choices=gender_choice, default='Men')

    def discount_price(self):
        return "{:.2f}".format(self.price - ((self.price * self.discount)/100))

    def __str__(self):
        return self.name
        
class Reviews(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_quantity = models.IntegerField()

    @property
    def get_total(self):
        total = float(self.product.discount_price()) * self.added_quantity
        return total



class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    total_amount = models.FloatField()
    payment_method = models.CharField(max_length=30, choices=payment_choices, default='Cash On Delivery')

    def __str__(self):
        return f"{self.id}     {self.customer.user}"

class Invoice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_DEFAULT, default=0)
    product_quantity = models.IntegerField()

class Favourites(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

class WishList(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)