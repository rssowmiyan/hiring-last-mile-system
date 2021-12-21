from pprint import pp, pprint
from django import forms
from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from funnels.forms import SequenceForm,FunnelForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from django.shortcuts import get_object_or_404,get_list_or_404
from .models import Funnel,Sequence
from contacts.models import ContactInfo
from datetime import date
import re
from django.db.models import Q

# sendgrid related imports
from sendgrid import SendGridAPIClient
import os
from sendgrid.helpers.mail import *
from decouple import config
#----------------------------------------------------
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
          return HttpResponse('<h1>Scheduling done</h1>')

def sendgrid(to_email,fillin_template,mail_subject,request):
     sg = SendGridAPIClient(api_key=config('SENDGRID_API_KEY')) 
     from_email = Email("sowmiyan00@gmail.com") 
     to_email = To(to_email)    
     subject = mail_subject
     content = Content("text/plain",fillin_template)
     mail = Mail(from_email, to_email, subject, content)
     response = sg.client.mail.send.post(request_body=mail.get())
     print(f'status_code->{response.status_code}')
     print(response.body,'\n')
     print(response.headers,'\n')

def startfunnel(request):
     objs = Funnel.objects.filter(ongoing='D') # getting inactive funnels
     today = date.today()
     today_date = today.strftime("%b %d, %Y")
     for obj in objs:
          if(obj.start_date == today_date): # checking the date
               pending_sequences = get_object_or_404(Sequence,funnel_id=obj.id) #getting the related sequences
               mail_subject = pending_sequences.description
               chosen_template = str(pending_sequences.sequence)
               merged_fields = re.findall(r"\{([A-Z a-z _]+)\}", chosen_template)
               # Creating a dict to replace placeholders in template
               d = {}
               for merged_field in merged_fields:
                    if(merged_field=='segment' or merged_field=='sub_segment'):
                         d[merged_field] = getattr(obj,merged_field) 
               # Filtering records that matches the segment & sub_segment
               matched_records = ContactInfo.objects.filter(Q(segment__icontains=obj.segment)&Q(sub_segment__icontains=obj.sub_segment))
               for matching_record in matched_records:
                    for merged_field in merged_fields:
                         if(merged_field not in ['segment','sub_segment']):
                              d[merged_field]=getattr(matching_record,merged_field)
                    fillin_template = chosen_template.format(**d)
                    to_email = getattr(matching_record,'email')
                    print('\n Entering sendgrid module \n')
                    pprint(fillin_template)
                    sendgrid(to_email,fillin_template,mail_subject,request)
     return HttpResponse('<h1>Emails sent!</h1>')


def viewcompleted(request):
     if(request.method=='GET'):
          com_funnels = Funnel.objects.filter(ongoing='C')
          return render(request,'completedfunnels.html',{'com_funnels':com_funnels})










