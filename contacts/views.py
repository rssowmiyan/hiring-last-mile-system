from os import name
from django.shortcuts import redirect, render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from contacts.models import Upload,ContactInfo
from .forms import UploadForm,ContactInfoForm
from django.http import HttpResponse
import pandas as pd
from pprint import pprint
from django.contrib.auth.decorators import login_required
from pathlib import Path
# ------------------------------------------------------------------------------------ #
def home(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            temp = form.save()
            print(temp.upload_file.url)
            # storing the filename uploaded in this session
            request.session['filepath'] = temp.upload_file.url
            return redirect('contacts:offerAChoice')
    else:
        form = UploadForm()
        return render(request,'contacts/home.html',{'form':form})



@login_required(login_url='/')
def offerAChoice(request):
    path_to_file = f'./media/{request.user.username}.txt'
    path = Path(path_to_file)
    '''
    if path.is_file(): # return true if the file exists
        return render('contacts/offerachoice.html')
    else: # If the file doesn't exists we'll jump to the fields matching process 
        return redirect('contacts:matchFields')
    '''
    return render(request,'contacts/offerachoice.html')

@login_required(login_url='/')
def matchFields(request):
    if(request.method=='POST'):
        filepath = request.session.get('filepath')
        if(filepath[-3:]=='csv'):
            print();pprint(f'extension -> {filepath[-3:]}')
            filepath = f'.{filepath}'
            df = pd.read_csv(filepath)
        else:  
            # converting excel to csv and then to dataframe
            print();pprint(f'extension -> {filepath[-4:]}')
            filepath = f'.{filepath}'
            df = pd.read_excel('filepath')
            df.to_csv('filepath',index=False)
        df.drop(df.filter(regex="Unnamed"),axis=1, inplace=True)
        names = list(df.columns)
        if request.POST.get('checkBox') == None:  # Don't use  prev key value pair
            matched = { key:request.POST.get(key, False) for key in names }
            # saving the mappings done by the user 
            path_to_file = f'./media/{request.user.username}.txt'
            keyvaluepair_file = open('path_to_file', 'wt+')
            keyvaluepair_file.write(str(matched))
            keyvaluepair_file.close()
        else: # Use the prev key value pair
            pass
        df.rename(columns = matched, inplace = True)
        df.set_index("full_name",drop=True)
        dictionary = df.to_dict(orient='index')
        # for index, object in dictionary.items():
        #     model = ContactInfo()
        #     for key,value in object.items():
        #         setattr(model, key, value)
        #     setattr(model, 'index', index)
        #     model.save()
        return HttpResponse('<h1>cols renamed!</h1>')

    else:
        filepath = request.session.get('filepath')
        filepath = f'.{filepath}'
        df = pd.read_csv(filepath)
        df.drop(df.filter(regex="Unnamed"),axis=1, inplace=True) # drop unnamed fields
        names = list(df.columns) # show the cols in the uploaded excel sheet
        # pprint(names)
        fields = [field.name for field in ContactInfo._meta.get_fields()]
        fields = sorted(fields,key=str.lower)
        # pprint(f'fields of the DB-> {fields}')
        return render(request,'contacts/matching.html',{'names':names,'fields':fields})

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


