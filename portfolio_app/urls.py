from django.urls import path
from . import views

app_name = "portfolio_app"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("projects/", views.ProjectListView.as_view(), name="project"),
    path("articles/", views.ArticleListView.as_view(), name="article"),
    path("contact/", views.ContactView.as_view(), name="contact")
]