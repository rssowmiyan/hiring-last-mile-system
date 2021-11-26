from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import NewUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = NewUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = NewUser
        fields = ('email',)
