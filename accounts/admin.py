from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = CustomUser
    list_display = [ #ModelAdmin.list_display
    "email", #To control which fields are displayed on the change  #list page of the admin
    "first_name",
    "last_name",
    "username",
    "is_staff",
    ]
    search_fields = ('username', 'first_name', 'last_name')
# fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("email","first_name","last_name","username")}),)
# add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("email","first_name","last_name","username")}),)
admin.site.register(CustomUser, CustomUserAdmin)