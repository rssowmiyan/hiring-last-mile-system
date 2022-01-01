from sendgrid import SendGridAPIClient
import os
from sendgrid.helpers.mail import *
from decouple import config
#-----------------------------------------------------------

sg = SendGridAPIClient(api_key=config('SENDGRID_API_KEY')) 
from_email = Email("tinktankstudio@gmail.com") 
to_email = To("")    
subject = "Testing message"
content = Content("text/html", '<p><span style="color: #202124; font-family: arial, sans-serif; font-size: 16px; background-color: #ffffff;">Dear barath, Congratulations on your offer! We are delighted to offer you the position of SDE with an anticipated start date 2nd Feb 2022. As discussed, please find attached your detailed offer letter.</span></p>')
mail = Mail(from_email, to_email, subject, content)
response = sg.client.mail.send.post(request_body=mail.get())

print(response.status_code)
print(response.body)
print(response.headers)