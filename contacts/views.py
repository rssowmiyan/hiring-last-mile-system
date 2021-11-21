from django.shortcuts import render


def home(request):
    return render(request,'contacts/home.html')

def matchFields(request):
    pass

def manualEntry(request):
    pass
