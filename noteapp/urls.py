from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views
from accounts.decorators import unauthenticated_user
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', unauthenticated_user(LoginView.as_view()), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('home', views.home, name='home'),
    path('', include('accounts.urls')),
    path('', include('notes.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
