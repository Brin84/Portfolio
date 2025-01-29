# from django.contrib.messages.context_processors import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, View, ListView, DetailView
from django.contrib import messages

from .models import Project, Article


class HomeView(TemplateView):
    template_name = 'portfolio_app/home.html'


class ProjectListView(ListView):
    model = Project
    template_name = 'portfolio_app/projects.html'
    context_object_name = 'projects'


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'portfolio_app/project_detail.html'
    context_object_name = 'project'

    def get_object(self):
        project_id = self.kwargs.get('pk')
        print(f"Запрос статьи с ID: {project_id}")

        try:
            return super().get_object()
        except Project.DoesNotExist:
            messages.info(self.request, "На данный момент проектов нет.")
            return redirect('portfolio_app:projects')


class ArticleListView(ListView):
    model = Article
    template_name = 'portfolio_app/articles.html'
    context_object_name = 'articles'


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'portfolio_app/article_detail.html'
    context_object_name = 'article'

    def get_object(self):
        project_id = self.kwargs.get('pk')
        print(f"Запрос статьи с ID: {project_id}")

        try:
            return super().get_object()
        except Article.DoesNotExist:
            messages.info(self.request, "На данный момент статей нет.")
            return redirect('portfolio_app:articles')


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

class Custom404View(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'portfolio_app/404.html', status=404)
