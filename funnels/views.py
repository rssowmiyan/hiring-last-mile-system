from pprint import pp, pprint
from django import forms
from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from funnels.forms import SequenceForm,FunnelForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from django.shortcuts import get_object_or_404 
from .models import Funnel

def starterforfunnel(request):     
     return render(request,'starterforfunnel.html')

def createfunnel(request):
     if(request.method=='POST'):
          form1 = FunnelForm(request.POST)
          if(form1.is_valid()):
               curr_form = form1.save()
               request.session['funnelID'] = curr_form.id
               return HttpResponseRedirect(reverse('funnels:createsequence'))
     else:
          form1 = FunnelForm()
          form2 = SequenceForm()
          return render(request,'createfunnel.html',{'form1':form1})

def createsequence(request):
     if(request.method=='POST'):
          form2 = SequenceForm(request.POST)
          # getting obj of the funnel created
          funnel_instance = get_object_or_404(Funnel, id=request.session.get('funnelID'))
          if(form2.is_valid()):
               curr_seq = form2.save(commit=False)
               # setting the foreign key
               curr_seq.funnel_id = funnel_instance
               curr_seq.save()
               return HttpResponseRedirect(reverse('funnels:createsequence'))
     else:
          form2 = SequenceForm()
          return render(request,'createsequence.html',{'form2':form2})
 
# def enoughofsequences(request):
#      return HttpResponseRedirect(reverse('funnels:starterforfunnel'))


def schedulesequences(request):
     if(request.method=='POST'):
          start_date = request.POST['StartDate']
          funnel_instance = get_object_or_404(Funnel, id=request.session.get('funnelID'))
          funnel_instance.start_date = start_date
          funnel_instance.save()
          # pprint(f'start_date -> {start_date} type-> {type(start_date)}')
          return HttpResponse('<h1>Got date</h1>')