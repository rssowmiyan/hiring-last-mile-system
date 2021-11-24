from django import forms
from django.db import models
from django.db.models import fields
from .models import Upload,ContactInfo
from django_countries.widgets import CountrySelectWidget

class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ('full_name','first_name','middle_name','last_name','company','designation','email','aadhar_id','pancard_id','phone_number','location','gender','title','university','country','degree','passing_year','college','linkedin','facebook','instagram_id','industry','state','zipcode','total_exp','ctc','notes','remarks','next_act',)
        widgets = {'country': CountrySelectWidget()}

class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ('upload_file',)