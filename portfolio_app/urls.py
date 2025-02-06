from django.urls import path
from . import views

app_name = "portfolio_app"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("projects/", views.ProjectListView.as_view(), name="projects"),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path("articles/", views.ArticleListView.as_view(), name="articles"),
    path("articles/<int:pk>/", views.ArticleDetailView.as_view(), name="article_detail"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path('404/', views.Custom404View.as_view(), name='custom_404'),
    path('add_project/', views.ProjectCreateView.as_view(), name='add_project'),
    path('add_article/', views.ArticleCreateView.as_view(), name='add_article')
]
