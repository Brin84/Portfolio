from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

def custom_404(request, exception):
    return render(request, 'portfolio_app/404.html')


handler404 = custom_404

urlpatterns = [
    path('admin/', admin.site.urls),  # подключение админ маршрута
    path('', include("portfolio_app.urls")),  # подключение маршрута
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


