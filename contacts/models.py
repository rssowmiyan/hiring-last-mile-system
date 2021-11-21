from django.db import models

def setDefaultValue():
    return 'Yettoprocess'

class Upload(models.Model):
    upload_file  = models.FileField(upload_to='.')
    uploaded_at = models.DateTimeField(auto_now_add=True)
