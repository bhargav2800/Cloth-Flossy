from django.contrib import admin
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

color_choice = (
    ("red", "red"),
    ("blue", "blue"),
    ("yellow", "yellow"),
    ("black", "black"),
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
    name = models.CharField(max_length=50)
    image = models.ImageField()
    short_line = models.CharField(max_length=40)
    price = models.FloatField()
    discount = models.IntegerField()
    target_audience = models.CharField(max_length=10, choices=gender_choice, default='Men')
    no_of_purchases = models.IntegerField(default=0)


    def discount_price(self):
        return "{:.2f}".format(self.price - ((self.price * self.discount)/100))

    def __str__(self):
        return self.name

class sub_products(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    size = models.CharField(max_length=10, choices=size_choices, default='XL')
    color = models.CharField(max_length=10, choices=color_choice, default='red')
    description = models.TextField()


class Reviews(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(sub_products, on_delete=models.CASCADE)
    added_quantity = models.IntegerField()

    @property
    def get_total(self):
        total = float(self.product.product.discount_price()) * self.added_quantity
        return total

class Order(models.Model):
    payment_status_choices = (
        ('SUCCESS', 'SUCCESS'),
        ('FAILURE', 'FAILURE'),
        ('PENDING', 'PENDING'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    total_amount = models.FloatField()
    payment_method = models.CharField(max_length=30, default='Cash On Delivery')
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None)
    # related to razorpay
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=payment_status_choices, default='PENDING')

    def __str__(self):
        return f"{self.id}     {self.customer.user}"

class Invoice(models.Model):
    status_choices = (
        ('Not Packed', 'Not Packed'),
        ('Ready For Shipment', 'Ready For Shipment'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered')
    )
    status_refund = (
        ('Not Initiated', 'Not Initiated'),
        ('Initiated', 'Initiated'),
        ('Done', 'Done')
    )
    status_pickup = (
        ('Will Soon Pick Up the Product', 'Will Soon Pick Up the Product'),
        ('Pick Up Done', 'Pick Up Done')
    )

    # Order
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(sub_products, on_delete=models.SET_DEFAULT, default=0)
    product_quantity = models.IntegerField()
    brand_name = models.CharField(max_length=50)
    product_name = models.CharField(max_length=50)
    buy_price = models.FloatField()
    product_discount = models.IntegerField()
    product_size = models.CharField(max_length=10)
    product_color = models.CharField(max_length=15)
    order_status = models.CharField(max_length=20, choices=status_choices, default='Not Packed')
    order_delivery_date = models.DateTimeField(blank=True, null=True)

    # returned Product
    returned_status = models.BooleanField(default=False)
    returned_date = models.DateTimeField(blank=True, null=True)
    returned_reason = models.TextField(blank=True)
    pick_up_date = models.DateTimeField(blank=True, null=True)
    pick_up_status = models.CharField(max_length=30, choices=status_pickup, default='Will Soon Pick Up the Product')
    refund_status = models.CharField(max_length=20, choices=status_refund, default='Not Initiated')


    # Replaced Product
    replaced_status = models.BooleanField(default=False)
    replaced_date = models.DateTimeField(blank=True, null=True)
    replacement_reason = models.TextField(blank=True)
    replace_pickup_date = models.DateTimeField(blank=True, null=True)
    replace_pickup_status = models.CharField(max_length=30, choices=status_pickup, default='Will Soon Pick Up the Product')
    replace_delivery_date = models.DateTimeField(blank=True, null=True)
    replace_delivery_status = models.CharField(max_length=20, choices=status_choices, default='Not Packed')
    replace_product_size = models.CharField(max_length=10, blank=True)
    replace_product_color = models.CharField(max_length=15, blank=True)

class Favourites(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

class WishList(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)