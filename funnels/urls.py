from django.urls import path
from . import views
app_name = 'funnels'

urlpatterns=[
    path('',views.starterforfunnel,name='starterforfunnel'),
]