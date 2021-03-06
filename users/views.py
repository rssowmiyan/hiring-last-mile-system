from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UserChangeForm
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm
from .models import NewUser
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
# ------------------------------------------------------------------
def loginuser(request):
    if(request.user.is_authenticated):
        return HttpResponseRedirect(reverse('contacts:home'))

    if request.method == 'GET':
        return render(request, 'loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Username and password does not match')
            return HttpResponseRedirect(reverse('loginuser'))
            # return render(request, 'loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('contacts:home')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('contacts:home')


# def signupuser(request):
#     if(request.method=='GET'):
#         return render(request,'signupuser.html',{'UserCreationForm':UserCreationForm,'UserChangeForm':UserChangeForm})
#     else:
#         form = UserCreationForm(request.POST)
#         if(form.is_valid()):
#                curr_form = form.save()
#                return HttpResponseRedirect(reverse('loginuser'))

# def newuserdetails(request):
#     pass