from os import name
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls.base import reverse
from contacts.models import Upload,ContactInfo
from .forms import UploadForm,ContactInfoForm
from django.http import HttpResponse
import pandas as pd
from pprint import pprint
from django.contrib.auth.decorators import login_required
from pathlib import Path
import ast
import openpyxl
from django.contrib import messages
### Global Variables
df = None
names = None

# ------------------------------------------------------------------------------------ #
def home(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            temp = form.save()
            print(f"\033[34m{temp.upload_file.url}.\033[0m")
            # storing the filename uploaded in this session
            request.session['filepath'] = temp.upload_file.url
            return redirect('contacts:matchFields')
    else:
        form = UploadForm()
        return render(request,'contacts/home.html',{'form':form})


# check and return T/F if there's already a mapping done by the user
def offerAChoice(path_to_file)->bool:
    path = Path(path_to_file)
    return path.is_file()


@login_required(login_url='/')
def matchFields(request):
    if(request.method=='POST'):
        '''
        filepath = request.session.get('filepath')
        if(filepath[-3:]=='csv'):
            print();pprint(f'extension -> {filepath[-3:]}')
            filepath = f'.{filepath}'
            df = pd.read_csv(filepath)
        else:  
            # converting excel to csv and then to pandas dataframe
            print();pprint(f'extension -> {filepath[-4:]}')
            filepath = f'.{filepath}'
            df = pd.read_excel(filepath)
            df.to_csv(filepath,index=False)

        df.drop(df.filter(regex="Unnamed"),axis=1, inplace=True)
        names = list(df.columns)
        '''
        global df;global names
        if request.POST.get('checkBox') == None:  # Give a choice for the user if he doesn't want to use prev key value pair
            matched = { key:request.POST.get(key, False) for key in names }
            # saving the mappings done by the user 
            path_to_file = f'./media/{request.user.username}.txt'
            keyvaluepair_file = open('path_to_file', 'wt+')
            keyvaluepair_file.write(str(matched))
            keyvaluepair_file.close()

        else: # Use the prev key value pair requested by user
            path_to_file = f'./media/{request.user.username}.txt'
            file = open(path_to_file) 
            contents = file.read()
            matched = ast.literal_eval(contents)
        df.rename(columns = matched, inplace = True)
        df.set_index("full_name",drop=True)
        dictionary = df.to_dict(orient='index')
        for index, object in dictionary.items():
            model = ContactInfo()
            for key,value in object.items():
                setattr(model, key, value)
            setattr(model, 'index', index)
            model.save()
        messages.success(request, 'Uploaded to the DB')
        return HttpResponseRedirect(reverse('contacts:home'))

    else:
        # all csv/excel files are stored in media dir and named by username itself
        path_to_file = f'./media/{request.user.username}.txt'
        flag = offerAChoice(path_to_file)
        filepath = request.session.get('filepath')
        filepath = f'.{filepath}'

        # check if its csv or xlsx
        if(filepath[-3:]=='csv'):
            df = pd.read_csv(filepath)
        else:  
            # converting excel to csv and then to pandas dataframe
            df = pd.read_excel(filepath)
            df.to_csv(filepath,index=False)

        df.drop(df.filter(regex="Unnamed"),axis=1, inplace=True) # drop unnamed fields
        names = list(df.columns) # show the cols in the uploaded excel sheet
        pprint(names)
        fields = [field.name for field in ContactInfo._meta.get_fields()] # get contactDB fields
        fields = sorted(fields,key=str.lower)
        # change the file extension
        if(filepath[-4:]=='xlsx'):
            pnt_to_file = Path(filepath)
            pnt_to_file.rename(pnt_to_file.with_suffix('.csv'))

        # pprint(fields)
        return render(request,'contacts/matching.html',{'names':names,'fields':fields,'flag':flag})

@login_required(login_url='/')
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


