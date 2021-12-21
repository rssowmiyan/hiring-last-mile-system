from sendgrid import SendGridAPIClient
import os
from sendgrid.helpers.mail import *
from decouple import config
#-----------------------------------------------------------

sg = SendGridAPIClient(api_key=config('SENDGRID_API_KEY')) 
from_email = Email("sowmiyan00@gmail.com") 
to_email = To("junkyard404@protonmail.com")    
subject = "Testing message"
content = Content("text/plain", "some random content XYZ")
mail = Mail(from_email, to_email, subject, content)
response = sg.client.mail.send.post(request_body=mail.get())

print(response.status_code)
print(response.body)
print(response.headers)