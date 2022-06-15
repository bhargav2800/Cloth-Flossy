from pyexpat.errors import messages
from django.contrib import admin
from .models import User,Customer

# Register your models here.
class UpdateUser(admin.ModelAdmin):

    def get_fields(self, request, obj=None):
        if request.user.is_staff and not request.user.is_superuser:
            fields = ('username','email','last_login', 'first_name', 'last_name', 'is_active', 'date_joined')
        else:
            fields = list(super(UpdateUser, self).get_fields(request, obj))
        return fields

    # def get_form(self, request, obj=None, **kwargs):
    #     """Override the get_form and extend the 'exclude' keyword arg"""
    #     if request.method == 'GET':
    #         if request.user.is_staff and not request.user.is_superuser:
    #             kwargs.update({
    #                 'exclude': getattr(kwargs, 'exclude', tuple()) + ('password','is_superuser','groups','is_staff','user_permissions'),
    #             })
    #     return super(UpdateUser, self).get_form(request, obj, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_staff and not request.user.is_superuser:
                return self.readonly_fields + ('last_login','is_active','date_joined')
        return self.readonly_fields

    def get_queryset(self, request):
        if request.user.is_staff and not request.user.is_superuser:
            return User.objects.filter(email=request.user.email)
        else:
            return super().get_queryset(request)
admin.site.register(User,UpdateUser)
admin.site.register(Customer)