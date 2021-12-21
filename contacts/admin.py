from django.contrib import admin
from .models import Upload,ContactInfo

class ContactInfoAdmin(admin.ModelAdmin):
    model = ContactInfo
    search_fields = ('email', 'full_name',)
    ordering = ('full_name',)
    list_display = [f.name for f in ContactInfo._meta.fields]
    fieldsets = (
        ('Personal', {'fields': ('first_name', 'middle_name','last_name','full_name','email','location','gender','phone_number','country','zipcode','state')}),
        ('Work', {'fields': ('title','company', 'designation','industry','linkedin','facebook','instagram_id','total_exp','ctc','date_of_incorporation')}),
        ('Education', {'fields': ('university','college','department','degree','passing_year',)}),
        ('Other', {'fields': ('aadhar_id','pancard_id','notes','remarks','next_act','segment','sub_segment')}),
    )


admin.site.register(ContactInfo,ContactInfoAdmin)
admin.site.register(Upload)

