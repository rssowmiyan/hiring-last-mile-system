from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NewUser
from django.forms import TextInput, Textarea

admin.site.site_header='Hiring Last Mile System'
admin.site.index_title='Greetings!'

from .forms import CustomUserCreationForm, CustomUserChangeForm

class UserAdminConfig(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    search_fields = ('email', 'username',)
    list_filter = ('email', 'username', 'is_active', 'is_staff')
    ordering = ('-date_joined',)
    readonly_fields = ['date_joined']
    list_display = ('email', 'username',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'username','last_login','no_of_funnels')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_superuser',)}),
        ('Personal', {'fields': ('address','date_joined','footer_message','phone_number',)}),
    )
    formfield_overrides = {
        NewUser.address: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )

admin.site.register(NewUser,UserAdminConfig)
