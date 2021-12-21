from django.db import models
from django.db.models.aggregates import Count
from django_countries.fields import CountryField
from django.core.validators import FileExtensionValidator

class ContactInfo(models.Model):
    CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Transgender'),
    )
    full_name   = models.CharField(max_length=100)
    first_name  = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=30,blank=True,default="")
    last_name   = models.CharField(max_length=30,blank=True,default="")
    company     = models.CharField(max_length=30)
    designation = models.CharField(max_length=30,blank=True,default="")
    email       = models.EmailField(primary_key = True,max_length=62)
    aadhar_id   = models.CharField(max_length=15,blank=True,default="")
    pancard_id  = models.CharField(blank=True,max_length=10,default="")
    phone_number= models.CharField(unique=True,max_length=10)
    location    = models.TextField(max_length=500,default="")
    gender      = models.CharField(max_length=20,choices=CHOICES)
    title       = models.CharField(blank=True,max_length=50,default="")
    department  = models.CharField(blank=True,max_length=50,default="")
    university  = models.CharField(max_length=50,default="")
    degree      = models.CharField(max_length=50,default="")
    passing_year= models.CharField(blank=True,max_length=4,default="")
    college     = models.CharField(max_length=50,blank=True,default="")
    linkedin    = models.URLField(verbose_name = "LinkedIn URL",max_length=50,blank=True,default="")
    facebook    = models.URLField(verbose_name = "Facebook URL",max_length=50,blank=True,default="")
    instagram_id= models.CharField(blank=True,verbose_name = "Instagram ID",max_length=50,default="")
    industry    = models.CharField(blank=True,max_length=50,default="")
    country     = CountryField(blank_label='(select country)')
    state       = models.CharField(max_length=35)
    zipcode     = models.CharField(max_length=12)
    key_skills  = models.CharField(max_length=50)
    total_exp   = models.CharField(verbose_name = "Total Experience",default="",max_length=15)
    years_in_business = models.CharField(blank=True,default="",max_length=4)
    cin_no      = models.CharField(blank=True,verbose_name="CIN NO",max_length=30,default="")
    turnover    = models.CharField(blank=True,max_length=30,default="")
    date_of_incorporation =  models.CharField(blank=True,default="",max_length=12)
    employees   = models.CharField(blank=True,default="",max_length=100)
    ctc         = models.CharField(max_length=10)
    notes       = models.TextField(blank=True,default="")
    remarks     = models.TextField(blank=True,default="")
    next_act    = models.CharField(blank=True,max_length=100,default="")
    udf01       = models.CharField(blank=True,max_length=100,default="")
    udf02       = models.CharField(blank=True,max_length=100,default="")
    udf03       = models.CharField(blank=True,max_length=100,default="")
    udf04       = models.CharField(blank=True,max_length=100,default="")
    udf05       = models.CharField(blank=True,max_length=100,default="")
    udf06       = models.CharField(blank=True,max_length=100,default="")
    udf07       = models.CharField(blank=True,max_length=100,default="")
    udf08       = models.CharField(blank=True,max_length=100,default="")
    udf09       = models.CharField(blank=True,max_length=100,default="")
    udf10       = models.CharField(blank=True,max_length=100,default="")
    segment     = models.CharField(max_length=50,default="General",blank=True)
    sub_segment = models.CharField(max_length=50,blank=True)

    def __str__(self):
        return self.full_name


class Upload(models.Model):
    upload_file  = models.FileField(upload_to='.',validators=[FileExtensionValidator( ['csv','xlsx','xls'] ) ])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{str(self.upload_file)}'
