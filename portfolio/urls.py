from django.conf.urls import handler404
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


def custom_404(request, exception):
    return render(request, 'portfolio_app/404.html')


handler404 = custom_404

urlpatterns = [
    path('admin/', admin.site.urls),  # подключение админ маршрута
    path('', include("portfolio_app.urls")),  # подключение маршрута
]
