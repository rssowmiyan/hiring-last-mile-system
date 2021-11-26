from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from users import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login',views.loginuser,name="loginuser"),
    path('contacts/',include('contacts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

