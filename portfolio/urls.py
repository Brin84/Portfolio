from django.conf import settings  # Импортируем объект настроек проекта Django.
from django.conf.urls.static import static  # Импортируем функцию static для обработки статических файлов.
from django.contrib import admin  # Импортируем модуль администратора для настройки маршрута админ-панели.
from django.urls import path, include  # Импортируем функции path и include для определения маршрутов URL.
from django.shortcuts import render  # Импортируем функцию render для рендеринга HTML-шаблонов.
from django.contrib.auth import \
    views as auth_views  # Импортируем стандартные представления аутентификации с псевдонимом.
from django.contrib.auth.views import \
    LogoutView  # Импортируем представление LogoutView для обработки выхода из системы.


def custom_404(request, exception):  # Определяем функцию для обработки ошибок 404.
    return render(request, 'portfolio_app/404.html')  # Возвращаем страницу 404.html, используя функцию render.


handler404 = custom_404  # Устанавливаем custom_404 как обработчик ошибок 404.

urlpatterns = [  # Определяем список маршрутов URL для проекта.
    path('admin/', admin.site.urls),  # Подключение стандартного маршрута админ-панели.
    path('', include("portfolio_app.urls")),  # Подключение маршрутов из приложения portfolio_app.
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # Подключение маршрута для входа в систему, используя кастомный шаблон.
    path('logout/', LogoutView.as_view(), name='logout')  # Подключение маршрута для выхода из системы.
]

if settings.DEBUG:  # Если включен режим отладки (DEBUG).
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)  # Добавляем маршруты для обработки медиафайлов.
