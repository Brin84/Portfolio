from msilib.schema import ListView

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, View, ListView
from .models import Project

class HomeView(TemplateView):
    template_name = 'portfolio_app/home.html'
    # def get(self, request):
    #     return HttpResponse("Это главная страница")


class ProjectListView(ListView):
    model = Project
    template_name = 'portfolio_app/projects.html'
    context_object_name = "projects"
    # def get(self, request):
    #     return HttpResponse("Это страница проектов")


class ArticleListView(ListView):
    model = Project
    template_name = 'portfolio_app/articles.html'
    context_object_name = "articles"


class ContactView(View):
    def get(self, request):
        context = {'success': False}
        return render(request, 'portfolio_app/contact.html', context)

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        context = {'success': True}
        return render(request, 'portfolio_app/contact.html', context)