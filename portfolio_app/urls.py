from django.urls import path  # Импортируем функцию path из django.urls для определения маршрутов URL.
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import \
    views  # Импортируем модуль views из текущей директории, чтобы использовать представления, определенные в нем.
from .views import send_test_email
from . import api_views

app_name = "portfolio_app"  # Задаем пространство имен для приложения, чтобы различать URL-ы между разными приложениями.

urlpatterns = [  # Определяем список маршрутов URL для приложения.
    path("", views.HomeView.as_view(), name="home"),  # Главная страница сайта, вызывается представление HomeView.
    path("projects/", views.ProjectListView.as_view(), name="projects"),
    # Страница со списком проектов, вызывается ProjectListView.
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    # Детальная страница проекта, идентифицируемая по первичному ключу (pk), вызывается ProjectDetailView.
    path("articles/", views.ArticleListView.as_view(), name="articles"),
    # Страница со списком статей, вызывается ArticleListView.
    path("articles/<int:pk>/", views.ArticleDetailView.as_view(), name="article_detail"),
    # Детальная страница статьи, идентифицируемая по первичному ключу (pk), вызывается ArticleDetailView.
    path("contact/", views.ContactView.as_view(), name="contact"),  # Страница контактов, вызывается ContactView.
    path('404/', views.Custom404View.as_view(), name='custom_404'),  # Кастомная страница 404, вызывается Custom404View.
    path('add_project/', views.ProjectCreateView.as_view(), name='add_project'),
    # Страница для добавления нового проекта, вызывается ProjectCreateView.
    path('add_article/', views.ArticleCreateView.as_view(), name='add_article'),
    # Страница для добавления новой статьи, вызывается ArticleCreateView.
    path('send_email/', send_test_email, name='send_email'),
    path('session_test/', views.SessionTestView.as_view(), name='session_test'),
    path('api/projects/', api_views.ProjectListAPI.as_view(), name='api-projects'),
    path('api/add_project/', api_views.ProjectCreateAPI.as_view(), name='api-add_project'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
