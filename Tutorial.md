1. Создал папку в поисковике с названием Portfolio
2. Создал новый репозиторий в GitHub
3. Настроил соединение локального проекта portfolio с удаленным проектом в GitHub c
   помощью следующих команд:
    1. git init - для инициализации пакета portfolio.
    2. git add remote origin "ссылка на проект в GitHub"
    3. git add . - добавил все файлы
    4. git commit -m "коммент" - закомитил все файлы
    5. git push origin master - запушил все файлы в ветку master

4. Создал файл .gitignore, записал туда файлы .idea/ и venv
5. Создал проект с фреймворком Django с помощью команды:
   django-admin startproject portfolio_app .
6. После запуска проекта появился пакет portfolio_app
7. Добавил классы моделей:
   from django.db import models

class Project(models.Model):
title = models.CharField(max_length=200)  # Название проекта
description = models.TextField()  # описание проекта
link = models.URLField(blank=True, null=True)  # ссылка на проект
created_at = models.DateTimeField(auto_now_add=True)  # дата создания проекта

    def __str__(self):
        return self.title

class Article(models.Model):
title = models.CharField(max_length=200) # Название статьи
content = models.TextField() # описание статьи
created_at = models.DateTimeField(auto_now_add=True)  # дата создания статьи

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
name = models.CharField(max_length=100)
email = models.EmailField()
message = models.TextField()
created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Сообщение от {self.name}"

8. Создал миграции с помощью команды:
   python manage.py makemigrations

9. Применил миграции с помощью команды:
   python manage.py migrate

10. Создал классы представления и шаблоны.
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
11. Настроил url-адреса для маршрутизации запросов к представлениям:
from django.urls import path
from . import views


app_name = "portfolio_app"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("projects/", views.ProjectListView.as_view(), name="projects"),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name= 'project_detail'),
    path("articles/", views.ArticleListView.as_view(), name="articles"),
    path("articles/<int:pk>/", views.ArticleDetailView.as_view(), name="article_detail"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path('404/', views.Custom404View.as_view(), name='custom_404')
]

12. Создал файлы html для нужных классов представления поместив их в папку templates/portfolio_app:

   Для projects:
{% extends 'portfolio_app/base.html' %}

{% block title %}Проекты{% endblock %}

{% block content %}
<h1 class="page-title">Мои проекты</h1>
<div class="projects-container">
    {% for project in projects %}
    <div class="project-item">
        {% if project.image %}
        <div class="project-image">
            <img src="{{ project.image.url }}" alt="{{ project.title }}"
                 style="width: 100%; height: auto; border-radius: 8px;">
        </div>
        {% endif %}
        <h2>{{ project.title }}</h2>
        <p>{{ project.description }}</p>
        <a href="{% url 'portfolio_app:project_detail' project.id %}">Подробнее</a>
    </div>
    {% empty %}
    <p>На данный момент у вас нет проектов!</p>
    {% endfor %}
</div>
{% endblock %}

   Для project-detail:
   {% extends 'portfolio_app/base.html' %}

{% block title %}{{ project.title }}{% endblock %}

{% block content %}
<div class="project-detail">
    <h1 class="page-title">{{ project.title }}</h1>

    <div class="project-content">
        {% if project.image %}
        <div class="project-image">
            <img src="{{ project.image.url }}" alt="{{ project.title }}"
                 style="width: 100%; max-width: 600px; height: auto; border-radius: 8px;">
        </div>
        {% endif %}

        <div class="project-description">
            <p>{{ project.description }}</p>
            {% if project.link %}
            <p>
                <a href="{{ project.link }}" target="_blank" class="button-link">Перейти по ссылке</a>
            </p>
            {% endif %}
        </div>
    </div>

    <div class="project-back">
        <a href="{% url 'portfolio_app:projects' %}" class="button-back">Назад к списку проектов</a>
    </div>
</div>
{% endblock %}

   Для home:
   {% extends 'portfolio_app/base.html' %}

{% block title %}Главная{% endblock %}

{% block content %}
<h1>Добро пожаловать на мой сайт портфолио!</h1>
<p>Здесь вы найдете информацию о моих проектах, статьях и способах связаться со мной.</p>
{% endblock %}

   Для articles:
   {% extends 'portfolio_app/base.html' %}

{% block title %}Статьи{% endblock %}

{% block content %}
<div class="articles-page">
    <h1 class="page-title">Мои статьи</h1>

    {% if messages %}
    <div class="messages-container">
        {% for message in messages %}
        <div class="message">
            {{ message }}
        </div>
        {% endfor %}
    </div>
    {% endif %}

    <div class="articles-container">
        {% for article in articles %}
        <div class="article-item">
            <h2 class="article-title">{{ article.title }}</h2>
            <p class="article-excerpt">{{ article.content|truncatewords:30 }}</p>
            <a href="{% url 'portfolio_app:article_detail' article.id %}" class="button-read-more">Читать далее</a>
        </div>
        {% empty %}
        <p class="no-articles">На данный момент статей нет.</p>
        {% endfor %}
    </div>
</div>
{% endblock %}

   Для article_detail:
   {% extends 'portfolio_app/base.html' %}

{% block title %}{{ article.title }}{% endblock %}

{% block content %}
<div class="article-detail-page">
    <h1 class="article-title">{{ article.title }}</h1>

    {% if article.image %}
    <div class="article-image-container">
        <img src="{{ article.image.url }}" alt="{{ article.title }}" class="article-image">
    </div>
    {% endif %}

    <div class="article-content">
        <p>{{ article.content }}</p>
    </div>

    <div class="back-link-container">
        <a href="{% url 'portfolio_app:articles' %}" class="button-back">Назад к списку статей</a>
    </div>
</div>
{% endblock %}

   Для base:
   <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Портфолио{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/styles.css' %}">
</head>
<body>
<header>
    <nav>
        <ul class="nav-list">
            <li class="{% if request.resolver_match.url_name == 'portfolio_app:home' %}active{% endif %}">
                <a href="{% url 'portfolio_app:home' %}">Главная</a>
            </li>
            <li class="{% if request.resolver_match.url_name == 'portfolio_app:projects' %}active{% endif %}">
                <a href="{% url 'portfolio_app:projects' %}">Проекты</a>
            </li>
            <li class="{% if request.resolver_match.url_name == 'portfolio_app:articles' %}active{% endif %}">
                <a href="{% url 'portfolio_app:articles' %}">Статьи</a>
            </li>
            <li class="{% if request.resolver_match.url_name == 'portfolio_app:contact' %}active{% endif %}">
                <a href="{% url 'portfolio_app:contact' %}">Контакты</a>
            </li>
        </ul>
    </nav>
</header>

<main>
    <!-- Блок для отображения изображений -->
    {% block media %}
    {% if image|default:'' %}
    <div class="media-container">
        <img src="{{ image.url }}" alt="Медиафайл" class="media-image">
    </div>
    {% endif %}
    {% endblock %}

    <!-- Основной контент страницы -->
    {% block content %}
    <p>Содержимое будет здесь.</p>
    {% endblock %}
</main>

<footer>
    <p>&copy; Мое портфолио </p>
</footer>
</body>
</html>

   Для cintact:
   {% extends 'portfolio_app/base.html' %}

{% block title %}Контакты{% endblock %}

{% block content %}
<div class="contact-page">
    <h1>Связаться со мной</h1>

    {% if success %}
    <div class="success-message">
        <p>Ваше сообщение отправлено!</p>
    </div>
    {% else %}
    <form method="post" class="contact-form">
        {% csrf_token %}

        <div class="form-group">
            <label for="name">Имя:</label>
            <input type="text" id="name" name="name" required>
        </div>

        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
        </div>

        <div class="form-group">
            <label for="message">Сообщение:</label>
            <textarea id="message" name="message" required></textarea>
        </div>

        <button type="submit" class="submit-button">Отправить</button>
    </form>
    {% endif %}
</div>
{% endblock %}

   Для ошибки 404:
   {% extends 'portfolio_app/base.html' %}

{% block title %}Страница не найдена{% endblock %}

{% block content %}
<h1>Страница не найдена</h1>
<p>Извините, запрашиваемая страница не существует.</p>
<a href="{% url 'portfolio_app:projects' %}">Назад к списку проектов</a>
{% endblock %}


