from django.urls import path
from . import views
app_name = 'contacts'

urlpatterns=[
    path('',views.home,name='home'),
    path('manual/',views.manualEntry,name='manualEntry'),
    path('uploaded/',views.matchFields,name='matchFields'),
]