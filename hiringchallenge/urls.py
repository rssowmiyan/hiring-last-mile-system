from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from users import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.loginuser,name="loginuser"),
    path('logout/',views.logoutuser,name="logoutuser"),
    path('contacts/',include('contacts.urls')),
    path('funnels/',include('funnels.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

