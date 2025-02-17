from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, ListView, DetailView, CreateView
from django.contrib import messages
from .forms import ProjectForm, ArticleForm, SearchForm
from .models import Project, Article, ContactMessage


class HomeView(TemplateView):
    template_name = 'portfolio_app/home.html'


class ProjectListView(ListView):
    model = Project
    template_name = 'portfolio_app/projects.html'
    context_object_name = 'projects'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query', '')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)  # Передаём форму в контекст
        return context


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
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query', '')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)  # Передаём форму в контекст
        return context


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

        ContactMessage.objects.create(name=name, email=email, message=message)

        context = {'success': True}
        return render(request, 'portfolio_app/contact.html', context)


class Custom404View(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'portfolio_app/404.html', status=404)


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'portfolio_app/add_project.html'
    # login_url = 'portfolio_app/projects.html'
    success_url = reverse_lazy('portfolio_app/projects')

    def get_success_url(self):
        return reverse_lazy('portfolio_app:projects')

    def form_valid(self, form):
        messages.success(self.request, "Проект добавлен")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка, проект не добавлен')
        return super().form_invalid(form)


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'portfolio_app/add_article.html'
    # login_url = 'portfolio_app/articles.html'
    success_url = reverse_lazy('portfolio_app:articles')

    def get_success_url(self):
        return reverse_lazy('portfolio_app:articles')

    def form_valid(self, form):
        messages.success(self.request, "Статья добавлена")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка, статья не добавлена')
        return super().form_invalid(form)
