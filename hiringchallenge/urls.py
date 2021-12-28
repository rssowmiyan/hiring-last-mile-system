from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from users import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.loginuser,name="loginuser"),
    path('logout/',views.logoutuser,name="logoutuser"),
    # path('signup/',views.signupuser,name='signupuser'),
    path('contacts/',include('contacts.urls')),
    path('funnels/',include('funnels.urls')),  
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

