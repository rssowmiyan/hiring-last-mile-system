from os import name
from django.shortcuts import redirect, render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from contacts.models import Upload,ContactInfo
from .forms import UploadForm,ContactInfoForm
from django.http import HttpResponse
import pandas as pd
from pprint import pprint
# ------------------------------------------------------------------------------------ #
def home(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            temp = form.save(commit=False)
            print(temp.upload_file.url)
            # storing the filename uploaded in this session
            request.session['filepath'] = temp.upload_file.url
            return redirect('contacts:matchFields')
    else:
        form = UploadForm()
        return render(request,'contacts/home.html',{'form':form})

def matchFields(request):
    if(request.method=='POST'):
        # filepath = '/media/testing123.csv'
        filepath = request.session.get('filepath')
        if(filepath[-3:]=='csv'):
            filepath = f'.{filepath}'
            df = pd.read_csv(filepath)
        # converting excel to csv and then to dataframe
        else:
            filepath = f'.{filepath}'
            df = pd.read_excel('filepath')
            df.to_csv('filepath', index=False)
        names = list(df.columns)
        matched = { key:request.POST.get(key, False) for key in names }
        # pprint(matched)
        df.rename(columns = matched, inplace = True)
        df.set_index("full_name")
        dictionary = df.to_dict(orient='index')
        pprint(f'dictionary->{dictionary}')
        for index, object in dictionary.items():
            model = ContactInfo()
            for key,value in object.items():
                setattr(model, key, value)
            setattr(model, 'index', index)
            model.save()
        return HttpResponse('<h1>cols renamed!</h1>')

    else:
        filepath = request.session.get('filepath')
        # filepath = '/media/testing123.csv'
        filepath = f'.{filepath}'
        df = pd.read_csv(filepath)
        # cols in the uploaded excel sheet
        names = list(df.columns)
        fields = [field.name for field in ContactInfo._meta.get_fields()]
        # pprint(f'fields of the DB-> {fields}')
        return render(request,'contacts/matching.html',{'names':names,'fields':fields,'filepath':filepath})


def manualEntry(request):
    if(request.method=='GET'):
        form = ContactInfoForm()
        return render(request,'contacts/fillupform.html',{'form':form})
    else:
        form = ContactInfoForm(request.POST)
        if(form.is_valid()):
            form.save()
            return HttpResponse('Homepage')
        else:
            return render(request,'fillupform.html',{'form':form})
