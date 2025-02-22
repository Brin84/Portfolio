import traceback

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, ListView, DetailView, CreateView
from django.contrib import messages
from .forms import ProjectForm, ArticleForm, SearchForm, ContactForm
from .models import Project, Article, ContactMessage


class HomeView(TemplateView):  # Определяем класс HomeView, наследуемый от TemplateView
    template_name = 'portfolio_app/home.html'  # Указываем путь к шаблону, который будет отображаться


class ProjectListView(ListView):  # Определяем класс представления, наследуя от ListView
    model = Project  # Указываем модель, с которой будет работать представление
    template_name = 'portfolio_app/projects.html'  # Указываем шаблон для отображения
    context_object_name = 'projects'  # Имя контекста, под которым будут переданы объекты в шаблон
    paginate_by = 3  # Устанавливаем пагинацию, ограничивая число объектов на одной странице до 3

    def get_queryset(self):  # Переопределяем метод получения набора данных
        queryset = super().get_queryset()  # Получаем базовый набор данных с помощью родительского метода
        query = self.request.GET.get('query', '')  # Получаем параметр запроса 'query' из строки запроса
        if query:  # Проверяем, был ли введён поисковый запрос
            queryset = queryset.filter(  # Фильтруем набор данных
                Q(title__icontains=query) | Q(description__icontains=query)
                # Поиск по заголовку или описанию, игнорируя регистр
            )
        return queryset  # Возвращаем отфильтрованный набор данных

    def get_context_data(self, **kwargs):  # Переопределяем метод получения контекста
        context = super().get_context_data(**kwargs)  # Получаем базовый контекст с помощью родительского метода
        context['form'] = SearchForm(
            self.request.GET)  # Добавляем форму поиска в контекст, передавая в неё текущие GET-параметры
        return context  # Возвращаем обновлённый контекст


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'portfolio_app/project_detail.html'
    context_object_name = 'project'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        try:
            # Попытка получить объект
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            messages.info(request, 'Проекта с указанным ID не существует')
            return redirect('portfolio_app:projects')
        return super().get(request, *args, **kwargs)



class ArticleListView(ListView):  # Определяем класс представления, наследуя от ListView
    model = Article  # Указываем модель, экземпляры которой будут отображаться в списке
    template_name = 'portfolio_app/articles.html'  # Указываем шаблон для отображения списка объектов
    context_object_name = 'articles'  # Имя контекста, под которым список объектов будет передан в шаблон
    paginate_by = 3  # Устанавливаем пагинацию: количество объектов на странице

    def get_queryset(self):  # Переопределяем метод получения набора данных
        queryset = super().get_queryset()  # Получаем исходный набор данных из модели
        query = self.request.GET.get('query',
                                     '')  # Извлекаем значение параметра 'query' из GET-запроса (по умолчанию пустая строка)
        if query:  # Если параметр 'query' не пустой
            queryset = queryset.filter(  # Фильтруем набор данных
                Q(title__icontains=query) | Q(content__icontains=query)
                # Поиск по заголовку или содержимому, игнорируя регистр
            )
        return queryset  # Возвращаем отфильтрованный набор данных

    def get_context_data(self, **kwargs):  # Переопределяем метод для добавления данных в контекст
        context = super().get_context_data(**kwargs)  # Получаем исходный контекст
        context['form'] = SearchForm(
            self.request.GET)  # Создаем и передаем форму поиска в контекст, используя данные из GET-запроса
        return context  # Возвращаем обновленный контекст


class ArticleDetailView(DetailView):  # Определяем класс представления, наследуя от DetailView
    model = Article  # Указываем модель, объект которой будет отображаться в деталях
    template_name = 'portfolio_app/article_detail.html'  # Указываем шаблон для отображения объекта
    context_object_name = 'article'  # Имя контекста, под которым объект будет передан в шаблон

    def get_object(self):  # Переопределяем метод для получения конкретного объекта
        project_id = self.kwargs.get('pk')  # Извлекаем значение 'pk' (primary key) из URL-параметров
        print(f"Запрос статьи с ID: {project_id}")  # Печатаем ID статьи в консоль для отладки

        try:
            return super().get_object()  # Пытаемся вернуть объект, используя стандартный метод
        except Article.DoesNotExist:  # Обрабатываем исключение, если объект не найден
            messages.info(self.request, "На данный момент статей нет.")  # Отправляем сообщение пользователю
            return redirect('portfolio_app:articles')  # Перенаправляем пользователя на страницу со списком статей


class ContactView(View):  # Определяем класс представления, наследуя от базового класса View
    def get(self, request):  # Метод, обрабатывающий GET-запросы
        form = ContactForm()
        return render(request, 'portfolio_app/contact.html', {
            'form': form,
            'success': False
        })  # Возвращаем страницу с формой и контекстом

    def post(self, request):  # Метод, обрабатывающий POST-запросы
        form = ContactForm(request.POST)
        name = request.POST.get('name')  # Извлекаем значение 'name' из данных POST-запроса
        email = request.POST.get('email')  # Извлекаем значение 'email' из данных POST-запроса
        message = request.POST.get('message')  # Извлекаем значение 'message' из данных POST-запроса

        # Создаем новый объект ContactMessage и сохраняем его в базе данных
        ContactMessage.objects.create(name=name, email=email, message=message)

        context = {'success': True}  # Обновляем контекст, устанавливая 'success' в True
        try:
            send_mail(subject=f"Сообщение от {name}",
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,)
            return render(request, 'portfolio_app/contact.html', {
                'form': None,
                'success': True,
            })
        except Exception as e:
            error_trace = traceback.format_exc()
            print(error_trace)
            # error_message = f"Ошибка при отправке сообщения: {str(e)}"
        return render(request, 'portfolio_app/contact.html', {
            'form': form,
            'success': False
        })  # Возвращаем страницу с обновленным контекстом


class Custom404View(View):  # Определяем класс представления, наследуя от базового класса View
    def get(self, request, *args,
            **kwargs):  # Метод для обработки GET-запросов; принимает request и любые дополнительные позиционные и именованные аргументы
        # Возвращаем шаблон '404.html' с HTTP-статусом 404
        return render(request, 'portfolio_app/404.html', status=404)


class ProjectCreateView(CreateView):  # Определяем класс представления, наследуя от базового класса CreateView
    model = Project  # Указываем модель, с которой будет работать представление
    form_class = ProjectForm  # Указываем форму, которая будет использоваться для создания объекта
    template_name = 'portfolio_app/add_project.html'  # Указываем имя шаблона, который будет использоваться для отображения формы

    # login_url = 'portfolio_app/projects.html'  # Закомментированная строка,
    # которая могла бы указывать URL для перенаправления неавторизованных пользователей

    success_url = reverse_lazy(
        'portfolio_app/projects')  # Указываем URL для перенаправления после успешного создания объекта

    def get_success_url(self):  # Метод для получения URL перенаправления после успешного создания объекта
        return reverse_lazy(
            'portfolio_app:projects')  # Возвращает URL с использованием reverse_lazy, чтобы избежать проблем с циклическим импортом

    def form_valid(self, form):  # Метод, вызываемый, если форма прошла валидацию
        messages.success(self.request, "Проект добавлен")  # Добавляем сообщение об успехе в систему сообщений
        return super().form_valid(form)  # Вызываем родительский метод form_valid, чтобы завершить обработку формы

    def form_invalid(self, form):  # Метод, вызываемый, если форма не прошла валидацию
        messages.error(self.request, 'Ошибка, проект не добавлен')  # Добавляем сообщение об ошибке в систему сообщений
        return super().form_invalid(form)  # Вызываем родительский метод form_invalid, чтобы обработать невалидную форму


class ArticleCreateView(
    CreateView):  # Создаем класс ArticleCreateView, наследуя его от CreateView, чтобы реализовать функционал для создания объектов.
    model = Article  # Назначаем модель Article, которую будет использовать это представление для создания объектов.
    form_class = ArticleForm  # Указываем класс формы ArticleForm, которая будет использоваться для ввода данных для нового объекта.
    template_name = 'portfolio_app/add_article.html'  # Указываем путь к HTML-шаблону, который будет отображаться при открытии формы.

    # login_url = 'portfolio_app/articles.html'  # Эта строка закомментирована. Она могла бы использоваться,
    # чтобы задать URL для перенаправления неавторизованных пользователей.

    success_url = reverse_lazy(
        'portfolio_app:articles')  # Задаем URL, на который будет перенаправлен пользователь после успешного создания объекта.

    # Используем reverse_lazy для обратной маршрутизации URL.

    def get_success_url(self):  # Определяем метод для получения URL перенаправления после успешного создания объекта.
        return reverse_lazy(
            'portfolio_app:articles')  # Возвращаем URL с использованием reverse_lazy, чтобы избежать проблем с циклическим импортом.

    def form_valid(self, form):  # Определяем метод, который вызывается, если форма прошла валидацию.
        messages.success(self.request,
                         "Статья добавлена")  # Добавляем сообщение об успешном добавлении статьи в систему сообщений.
        return super().form_valid(
            form)  # Вызываем родительский метод form_valid, чтобы завершить обработку формы и сохранить объект.

    def form_invalid(self, form):  # Определяем метод, который вызывается, если форма не прошла валидацию.
        messages.error(self.request,
                       'Ошибка, статья не добавлена')  # Добавляем сообщение об ошибке в систему сообщений.
        return super().form_invalid(
            form)  # Вызываем родительский метод form_invalid, чтобы обработать невалидную форму и вернуть пользователя к форме.

def send_test_email(request):
    send_mail(
        'Бла-бла-бла, я пытаюсь работать.',
        'brin14071984@gmail.com',
        ['ascomfort84@gmail.com'],
    )
    return HttpResponse("письмо отправлено!")