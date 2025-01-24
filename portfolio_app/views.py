from msilib.schema import ListView

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, View, ListView
from .models import Project

class HomeView(View):
    # template_name = 'portfolio_app/home.html'
    def get(self, request):
        return HttpResponse("Это главная страница")


class ProjectListView(View):
    # model = Project
    # template_name = 'portfolio_app/home.html'
    # context_object_name = "project"
    def get(self, request):
        return HttpResponse("Это страница проектов")


class ArticleListView(View):
    def get(self, request):
        return HttpResponse("Это страница статьи")


class ContactView(View):
    def get(self, request):
        return HttpResponse("Это страница обратной связи")