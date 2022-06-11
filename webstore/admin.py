from pyexpat.errors import messages
from django.contrib import admin
from .models import User,Customer,Brand,Category,Product,Favourites,Wishlist,Reviews,Cart,Order,Invoice

# Register your models here.
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Category)

admin.site.register(Favourites)
admin.site.register(Wishlist)
admin.site.register(Reviews)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Invoice)

class brand_modify(admin.ModelAdmin):
    readonly_fields=('user',)
    def get_queryset(self, request):
        if request.user.is_staff and not request.user.is_superuser:
            Brand.user = request.user
            return Brand.objects.filter(user=request.user)
        else:
            Brand.user = request.user
            return super().get_queryset(request)

admin.site.register(Brand, brand_modify)

class product_modify(admin.ModelAdmin):
    readonly_fields=('brand',)
    def get_queryset(self, request):
        if request.user.is_staff and not request.user.is_superuser:
            Product.brand = request.user.brand
            return Product.objects.filter(brand=request.user.brand)
        else:
            Product.brand = request.user.brand
            return super().get_queryset(request)

admin.site.register(Product, product_modify)