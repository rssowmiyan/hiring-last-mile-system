from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _

class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, user_name,password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name,password,**other_fields)

    def create_user(self, email, user_name ,password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=user_name,**other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,blank=False)
    user_name = models.CharField(max_length=30, unique=True,blank=False)
    date_joined = models.DateTimeField(default=timezone.now)
    address = models.TextField(max_length=500, blank=True)
    phone_number = PhoneNumberField(unique = True, null = False, blank = False)
    is_staff = models.BooleanField(default=False,help_text='Designates whether the user can log intothis admin site.')
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    no_of_funnels = models.PositiveSmallIntegerField(default=0,validators=[
            MaxValueValidator(30),
        ])
    footer_message = models.TextField(max_length=500, blank=True)
    
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name',]
    
    def __str__(self) -> str:
        return self.user_name