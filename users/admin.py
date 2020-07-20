from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Address,AccountType
from .forms import CustomUserCreationForm
# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ['email','username',]
    
admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Address)
admin.site.register(AccountType)