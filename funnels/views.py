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
import re
from django.db.models import Q
from datetime import datetime,date,timedelta
# sendgrid related imports
from sendgrid import SendGridAPIClient
import os
from sendgrid.helpers.mail import *
from decouple import config
import time
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

          return HttpResponse('<h1>Scheduling done</h1>')

def sendgrid(to_email,fillin_template,mail_subject,request):
     sg = SendGridAPIClient(api_key=config('SENDGRID_API_KEY')) 
     from_email = Email("sowmiyan00@gmail.com") 
     to_email = To(to_email)    
     subject = mail_subject
     content = Content("text/plain",fillin_template)
     mail = Mail(from_email, to_email, subject, content)
     response = sg.client.mail.send.post(request_body=mail.get())
     print(f'\033[34mstatus code->{response.status_code}.\033[0m')
     print(response.body,'\n')
     print(response.headers,'\n')


def updatefunnel(seq):
     seq.funnel_id.seqs_remaining-=1
     if(seq.funnel_id.seqs_remaining==0):
          seq.funnel_id.status = 'C'
     else:
          seq.funnel_id.status = 'O'



def startfunnel(request):
     time.sleep(5)
     today_dateobj = date.today()
     seqs = Sequence.objects.filter(sch_date=today_dateobj)
     for seq in seqs:
          mail_subject = seq.description
          chosen_template = str(seq.sequence)
          merged_fields = re.findall(r"\{([A-Z a-z _]+)\}", chosen_template)

          # Creating a dict to replace placeholders in template
          d = {}
          for merged_field in merged_fields:
               if(merged_field=='segment' or merged_field=='sub_segment'):
                    d[merged_field] = getattr(seq.sequence,merged_field)

          # Filtering records that matches the segment & sub_segment
          matched_records = ContactInfo.fun_objects.filter(Q(segment__icontains=seq.sequence.segment)&Q(sub_segment__icontains=seq.sequence.sub_segment))

          # Iterating through the matchedrecords and fetching necessary details
          for matching_record in matched_records:
               for merged_field in merged_fields:
                    if(merged_field not in ['segment','sub_segment']):
                         d[merged_field]=getattr(matching_record,merged_field)
               fillin_template = chosen_template.format(**d) # generic template to personal one
               to_email = getattr(matching_record,'email')
               print("\033[34mEntering sendgrid module.\033[0m")
               pprint(fillin_template)
               sendgrid(to_email,fillin_template,mail_subject,request)

          updatefunnel(seq)
     return HttpResponse('<h1>Emails sent!</h1>')
     


def viewcompleted(request):
     if(request.method=='GET'):
          com_funnels = Funnel.objects.filter(status='C')
          return render(request,'completedfunnels.html',{'com_funnels':com_funnels})


def viewongoing(request):
     if(request.method=='GET'):
          ongoing_funnels = Funnel.objects.filter(status='O')
          return render(request,'',{'com_funnels':ongoing_funnels})

