from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.fields import CharField
from django.utils import timezone
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, username,password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username,password,**other_fields)

    def create_user(self, email, username ,password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username,**other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,blank=False)
    username = models.CharField(max_length=30, unique=True,blank=False)
    date_joined = models.DateTimeField(default=timezone.now)
    address = models.TextField(max_length=500, blank=True)
    phone_number = CharField(max_length=20)
    is_staff = models.BooleanField(default=False,help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    no_of_funnels = models.PositiveSmallIntegerField(default=0,validators=[
            MaxValueValidator(30),
        ])
    footer_message = models.TextField(max_length=500, blank=True)
    
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]
    
    def __str__(self) -> str:
        return self.username