from os import name
from django.urls import path
from . import views
app_name = 'contacts'

urlpatterns=[
    path('',views.home,name='home'),
    path('manual/',views.manualEntry,name='manualEntry'),
    path('match/',views.matchFields,name='matchFields'),
    path('choice/',views.offerAChoice,name='offerAChoice'),
]