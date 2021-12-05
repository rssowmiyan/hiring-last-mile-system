from django.contrib import admin
from .models import DefaultTemplates,Sequence,Funnel

admin.site.register(Funnel)
admin.site.register(DefaultTemplates)
admin.site.register(Sequence)

