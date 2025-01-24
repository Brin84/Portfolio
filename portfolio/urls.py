from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # подключение админ маршрута
    path('', include("portfolio_app.urls")) # подключение маршрута
]
