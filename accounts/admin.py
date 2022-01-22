from django.contrib import admin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser

# register custom user and admin to `admin/`
admin.site.register(CustomUser, CustomUserAdmin)
