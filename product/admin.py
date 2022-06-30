from django import forms
from django.contrib import admin
from django.forms import modelform_factory

from .models import Brand,Category,Product,Reviews,Cart,Order,Invoice, Favourites, WishList, sub_products

# Register your models here.
admin.site.register(Category)
admin.site.register(Reviews)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Invoice)

class Brand_Modify(admin.ModelAdmin):
    fields = ['brand_name','user']
    readonly_fields=('user',)
    def get_queryset(self, request):
        if request.user.is_staff and not request.user.is_superuser:
            Brand.user = request.user
            return Brand.objects.filter(user=request.user)
        else:
            Brand.user = request.user
            return super().get_queryset(request)

admin.site.register(Brand, Brand_Modify)

class Product_Modify(admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_staff and not request.user.is_superuser:
                return self.readonly_fields + ('brand',)
        return self.readonly_fields

    # def get_form(self, request, obj=None, **kwargs):
    #     # Proper kwargs are form, fields, exclude, formfield_callback
    #     if obj: # obj is not None, so this is a change page
    #         # kwargs['exclude'] = ['upload_file',]
    #         kwargs['fields'] = ['category', 'available_quantity', 'name', 'price', 'image', 'discount', 'description',
    #                             'no_of_purchases', 'product_size']
    #     else: # obj is None, so this is an add page
    #         kwargs['fields'] = ['category','available_quantity','name','price','image','discount','description','no_of_purchases','product_size']
    #     return super(Product_Modify, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if request.user.is_staff and not request.user.is_superuser:
            obj.brand = request.user.brand
            obj.last_modified_by = request.user.brand
            obj.save()
        else:
            obj.save()

    def get_queryset(self, request):
        if request.user.is_staff and not request.user.is_superuser:
            return Product.objects.filter(brand=request.user.brand)
        else:
            return super().get_queryset(request)

admin.site.register(Product, Product_Modify)


class SubProductAdminForm(forms.BaseModelFormSet):
    class Meta:
        model = sub_products
        fields = "__all__"

@admin.register(sub_products)
class ProductSubModify(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_staff and not request.user.is_superuser:
            form = super().get_form(request, obj, **kwargs)
            form.base_fields["product"]._queryset = Product.objects.filter(brand__user=request.user)
            return form
        elif request.user.is_superuser:
            return super().get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        if request.user.is_staff and not request.user.is_superuser:
            return sub_products.objects.filter(product__brand__user=request.user)
        else:
            return super().get_queryset(request)

admin.site.register(Favourites)
admin.site.register(WishList)