from django.contrib import admin
from Auth.models import User, Admin_info
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from Auth.forms import CustomUserCreationsForm,CustomuserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationsForm
    form = CustomuserChangeForm
    model = User
    list_display = ['email','is_staff','is_active','is_patient']
    list_filter = ['email','is_staff','is_active']

    fieldsets = (
     (None,{
         'fields':('email','password','uid','is_patient','is_superuser')}),
        ('permissions',{'fields':('is_staff','is_active')}),
    )

    add_fieldsets = (
     (None,{
         'fields':('wide',),
         'fields':('email','password1','password2','uid','is_staff','is_active','is_patient','is_superuser')
     }),
    )
    

    search_fields = ('email',)
    ordering = ('email',)


    



admin.site.register(User,CustomUserAdmin)
admin.site.register(Admin_info)
