from django.shortcuts import redirect, render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from contacts.models import Upload
from .forms import UploadForm
from django.http import HttpResponse
import pandas as pd
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
    filepath = request.session.get('filepath')
    filepath = f'.{filepath}'
    df = pd.read_csv(filepath)
    names = list(df.columns)
    fields = [field.name for field in MODEL_NAME._meta.get_fields()]
    return render(request,'contacts/matching.html')


def manualEntry(request):
    pass
