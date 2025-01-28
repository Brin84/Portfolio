from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, View, ListView, DetailView
from .models import Project, Article


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


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'portfolio_app/project_detail.html'
    context_object_name = 'project'


class ArticleListView(ListView):
    model = Article
    template_name = 'portfolio_app/articles.html'
    context_object_name = 'articles'


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


