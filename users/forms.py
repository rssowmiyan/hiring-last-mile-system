from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import NewUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = NewUser
        # fields = ('email','username','address','phone_number','no_of_funnels','footer_message')
        fields = '__all__'


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = NewUser
        fields = '__all__'
        
