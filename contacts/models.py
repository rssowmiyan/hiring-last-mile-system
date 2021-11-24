from django.db import models
from django.db.models.aggregates import Count
from django_countries.fields import CountryField
from django.core.validators import FileExtensionValidator
from django.core.validators import MinValueValidator, MaxValueValidator

class ContactInfo(models.Model):
    CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Transgender'),
    )
    full_name   = models.CharField(max_length=100)
    first_name  = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=30,blank=True)
    last_name   = models.CharField(max_length=30,blank=True)
    company     = models.CharField(max_length=30)
    designation = models.CharField(max_length=30,blank=True)
    email       = models.EmailField(unique=True,max_length=62)
    aadhar_id   = models.CharField(unique=True,max_length=15,blank=True,validators=[MinValueValidator(14),MaxValueValidator(14)])
    pancard_id  = models.CharField(blank=True,max_length=10)
    phone_number= models.CharField(unique=True,max_length=10)
    location    = models.TextField(max_length=500)
    gender      = models.CharField(max_length=20,choices=CHOICES)
    title       = models.CharField(blank=True,max_length=50)
    department  = models.CharField(blank=True,max_length=50)
    university  = models.CharField(max_length=50)
    degree      = models.CharField(max_length=50)
    passing_year= models.PositiveSmallIntegerField(blank=True,null=True)
    college     = models.CharField(max_length=50,blank=True)
    linkedin    = models.URLField(verbose_name = "LinkedIn URL",max_length=50,blank=True)
    facebook    = models.URLField(verbose_name = "Facebook URL",max_length=50,blank=True)
    instagram_id= models.CharField(blank=True,verbose_name = "Instagram ID",max_length=50)
    industry    = models.CharField(blank=True,max_length=50)
    country     = CountryField(blank_label='(select country)')
    state       = models.CharField(max_length=35)
    zipcode     = models.CharField(max_length=12,validators=[MinValueValidator(5)])
    key_skills  = models.CharField(max_length=50)
    total_exp   = models.PositiveSmallIntegerField(verbose_name = "Total Experience")
    years_in_business = models.PositiveSmallIntegerField(blank=True,null=True)
    cin_no      = models.CharField(blank=True,validators=[MinValueValidator(21),MaxValueValidator(21)],verbose_name="CIN NO",max_length=21)
    turnover    = models.CharField(blank=True,max_length=30)
    date_of_incorporation =  models.DateField(blank=True,null=True)
    employees   = models.PositiveIntegerField(blank=True,null=True)
    ctc         = models.PositiveSmallIntegerField()
    notes       = models.TextField(blank=True)
    remarks     = models.TextField(blank=True)
    next_act    = models.CharField(blank=True,max_length=100)
    udf01       = models.CharField(blank=True,max_length=100)
    udf02       = models.CharField(blank=True,max_length=100)
    udf03       = models.CharField(blank=True,max_length=100)
    udf04       = models.CharField(blank=True,max_length=100)
    udf05       = models.CharField(blank=True,max_length=100)
    udf06       = models.CharField(blank=True,max_length=100)
    udf07       = models.CharField(blank=True,max_length=100)
    udf08       = models.CharField(blank=True,max_length=100)
    udf09       = models.CharField(blank=True,max_length=100)
    udf10       = models.CharField(blank=True,max_length=100)

    def __str__(self):
        return self.full_name


class Upload(models.Model):
    upload_file  = models.FileField(upload_to='.',validators=[FileExtensionValidator( ['csv','xlsx','xls'] ) ])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{str(self.upload_file)}'
