from pprint import pprint
from typing import Counter
from django import forms
from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render,get_object_or_404
from funnels.forms import SequenceForm,FunnelForm,DefaultTemplatesForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from django.shortcuts import get_object_or_404,get_list_or_404
from .models import Funnel,Sequence,DefaultTemplates
from contacts.models import ContactInfo
import re
from django.db.models import Q
from django.db import IntegrityError
from datetime import datetime,date,timedelta
# sendgrid related imports
from sendgrid import SendGridAPIClient
import os
from sendgrid.helpers.mail import *
from decouple import config
import time
# messages
from django.contrib import messages
# usermodel
from django.contrib.auth import get_user_model
#----------------------------------------------------
@login_required(login_url='/')
def starterforfunnel(request):    
     return render(request,'starterforfunnel.html')

@login_required(login_url='/')
def createfunnel(request):
     if(request.method=='POST'):
          form1 = FunnelForm(request.POST)
          if(form1.is_valid()):
               curr_form = form1.save()
               request.session['funnelID'] = curr_form.id #We need it later for settingup seqs
               curr_form.created_by = request.user
               curr_form.save()
               # incrementing no of funnels created by user 
               request.user.no_of_funnels+=1
               request.user.save()
               return HttpResponseRedirect(reverse('funnels:createsequence'))
     else:
          form1 = FunnelForm()
          return render(request,'createfunnel.html',{'form1':form1})

@login_required(login_url='/')
def createsequence(request):
     if(request.method=='POST'):
          form2 = SequenceForm(request.POST)
          # getting obj of the funnel created
          funnel_instance = get_object_or_404(Funnel, id=request.session.get('funnelID'))
          if(form2.is_valid()):
               curr_seq = form2.save(commit=False)
               # setting the foreign key
               curr_seq.funnel_id = funnel_instance
               funnel_instance.no_of_seq+=1
               curr_seq.save()
               return HttpResponseRedirect(reverse('funnels:createsequence'))
     else:
          form2 = SequenceForm()
          return render(request,'createsequence.html',{'form2':form2})
 

@login_required(login_url='/')
def schedulesequences(request):
     if(request.method=='POST'):
          string_start_date = request.POST['StartDate']
          start_date = datetime.strptime(string_start_date,'%b %d, %Y').date()
          funnel_instance = get_object_or_404(Funnel, id=request.session.get('funnelID'))
          funnel_instance.start_date = start_date

          # calculating and saving it
          funnel_instance.seqs_remaining=funnel_instance.no_of_seq=Sequence.objects.filter(funnel_id=request.session.get('funnelID')).count()
          funnel_instance.save()

          # Generating dates for sequences associated with the funnel
          seqs = Sequence.objects.filter(funnel_id=request.session.get('funnelID'))
          for seq in seqs:
               seq.sch_date = start_date
               seq.save()
               start_date += timedelta(days=seq.frequency)
          messages.warning(request, 'Sequences Scheduled')
          return HttpResponseRedirect(reverse('funnels:starterforfunnel'))

def sendgrid(to_email,fillin_template,mail_subject,request):
     sg = SendGridAPIClient(api_key='') 
     from_email = Email("tinktankstudio@gmail.com") 
     to_email = To(to_email)    
     subject = mail_subject
     content = Content("text",fillin_template)
     mail = Mail(from_email, to_email, subject, content)
     response = sg.client.mail.send.post(request_body=mail.get())
     print(f'\033[34mstatus code->{response.status_code}.\033[0m')
     # print(response.body,'\n')
     # print(response.headers,'\n')


def updatefunnel(request,seq):
     try:
          curr_funnel = seq.funnel_id
          curr_funnel.seqs_remaining -=1
          curr_funnel.save()
          if(curr_funnel.seqs_remaining==0):
               seq.funnel_id.status = 'C'
          else:
               seq.funnel_id.status = 'O'
          seq.funnel_id.save()
     except IntegrityError:
          messages.add_message(request, messages.INFO, 'No pending funnels for today')
          return 'cancel'


@login_required(login_url='/')
def startfunnel(request):
     today_dateobj = date.today()
     seqs = Sequence.objects.filter(sch_date=today_dateobj)
     counter = 0
     for seq in seqs:
          flag_for_repeated_fun = updatefunnel(request,seq)
          if(flag_for_repeated_fun == 'cancel'):
               continue
          counter+=1
          mail_subject = seq.description
          chosen_template = str(seq.sequence)
          merged_fields = re.findall(r"\{([A-Z a-z _]+)\}", chosen_template)

          # Creating a dict to replace placeholders in template
          d = {}
          for merged_field in merged_fields:
               if(merged_field=='segment' or merged_field=='sub_segment'):
                    d[merged_field] = getattr(seq.funnel_id,merged_field)

          # Filtering records that matches the segment & sub_segment
          matched_records = ContactInfo.objects.filter(Q(segment__icontains=seq.funnel_id.segment)&Q(sub_segment__icontains=seq.funnel_id.sub_segment))

          # Iterating through the matchedrecords and fetching necessary details
          for matching_record in matched_records:
               for merged_field in merged_fields:
                    if(merged_field not in ['segment','sub_segment']):
                         d[merged_field]=getattr(matching_record,merged_field)
               fillin_template = chosen_template.format(**d) # generic template to personal one
               to_email = getattr(matching_record,'email')
               print("\033[34mEntering sendgrid module.\033[0m")
               # pprint(fillin_template)
               sendgrid(to_email,fillin_template,mail_subject,request)
          print('\033[34mUpdating funnels\033[0m')
     if(counter!=0):
          counter_msg = f'Emails are sent! {counter} sequence(s) found for today'
          messages.success(request,counter_msg)
     time.sleep(1)
     return HttpResponseRedirect(reverse('funnels:starterforfunnel'))
     


def viewcompleted(request):
     if(request.method=='GET'):
          com_funnels = Funnel.objects.filter(status='C')
          return render(request,'completedfunnels.html',{'com_funnels':com_funnels})


def viewongoing(request):
     if(request.method=='GET'):
          ongoing_funnels = Funnel.objects.filter(status='O')
          return render(request,'ongoingfunnels.html',{'ongoing_funnels':ongoing_funnels})


def viewinactive(request):
     if(request.method=='GET'):
          inactive_funnels = Funnel.objects.filter(status='D')
          return render(request,'inactivefunnels.html',{'inactive_funnels':inactive_funnels })

@login_required(login_url='/')
def customtemplate(request):
     if(request.method=='GET'):
          return render(request,'createtemplates.html')
     else:
          custom_template = request.POST.get('template_data', False)
          pprint(custom_template)
          obj = DefaultTemplates(template=custom_template)
          obj.save()
          messages.success(request, 'Template saved')
          return HttpResponseRedirect(reverse('funnels:starterforfunnel'))

@login_required(login_url='/')
def displaycustomtemplate(request):
     all_templates_objs = DefaultTemplates.objects.all()
     return render(request,'viewtemplates.html',{'objs':all_templates_objs})


@login_required(login_url='/')
def editcustomtemplate(request,customtem_pk):
     if(request.method=='GET'):
          selected_custom_template_obj = DefaultTemplates.objects.filter(id=customtem_pk).first()
          selected_custom_template_form = DefaultTemplatesForm(instance=selected_custom_template_obj)
          return render(request,'edittemplates.html',{'form':selected_custom_template_form})
     else:
          form = DefaultTemplatesForm(request.POST)
          form.save()
          return HttpResponseRedirect(reverse('funnels:starterforfunnel'))


