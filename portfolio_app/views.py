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
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class HomeView(TemplateView):  # Определяем класс HomeView, наследуемый от TemplateView
    template_name = 'portfolio_app/home.html'  # Указываем путь к шаблону, который будет отображаться


@method_decorator(cache_page(300), name='dispatch')
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
    # Указываем модель, с которой будет работать представление
    model = Project

    # Путь к HTML-шаблону для отображения детальной информации о проекте
    template_name = 'portfolio_app/project_detail.html'

    # Имя переменной контекста, которая будет использоваться в шаблоне
    # Позволяет обращаться к объекту проекта как 'project' в шаблоне
    context_object_name = 'project'

    def get_object(self, queryset=None):
        # Получаем первичный ключ (ID) проекта из URL
        pk = self.kwargs.get('pk')

        try:
            # Пытаемся найти объект проекта по первичному ключу
            # Метод .get() вызывает исключение, если объект не найден
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            # Если проект не найден, вызываем исключение Http404
            # Это приведет к отображению стандартной страницы 404
            raise Http404

    def get(self, request, *args, **kwargs):
        try:
            # Пытаемся получить объект проекта
            # Метод self.get_object() может вызвать Http404
            self.object = self.get_object()


        except Http404:
            # Обработка случая, когда проект не найден

            # Добавляем информационное сообщение для пользователя
            messages.info(request, 'Проекта с указанным ID не существует')

            # Перенаправляем пользователя на страницу со списком проектов
            return redirect('portfolio_app:projects')

        # Если проект найден, вызываем родительский метод get
        # Это стандартная обработка для DetailView
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
            'success': False,
            'spam_error': None
        })  # Возвращаем страницу с формой и контекстом

    def post(self, request):  # Метод, обрабатывающий POST-запросы
        form = ContactForm(request.POST)

        if not SpamProtection.check_rate_limit(request):
            return render(request, 'portfolio_app/contact.html', {
                'form': None,
                'success': False,
                'spam_error': 'Вы превысили лимит отправки сообщений. Для связи со мной:'
                              '<a href="https://t.me/AscomfortAlexander">Telegram</a>'
            })
        if form.is_valid():

            name = request.POST.get('name')  # Извлекаем значение 'name' из данных POST-запроса
            email = request.POST.get('email')  # Извлекаем значение 'email' из данных POST-запроса
            message = request.POST.get('message')  # Извлекаем значение 'message' из данных POST-запроса

            # Создаем новый объект ContactMessage и сохраняем его в базе данных
            ContactMessage.objects.create(name=name, email=email, message=message)

            # словарь контекста с флагом успешной операции
            context = {'success': True}

            try:
                # Отправка электронной почты с помощью Django send_mail
                send_mail(
                    # Тема письма - формируется с именем отправителя
                    subject=f"Сообщение от {name}",

                    # Текст сообщения, переданный в форме
                    message=message,

                    # Email отправителя из настроек проекта
                    from_email=settings.EMAIL_HOST_USER,

                    # Список получателей (берется из настроек)
                    recipient_list=[settings.CONTACT_EMAIL],

                    # Параметр для полной обработки ошибок
                    fail_silently=False,
                )

                # Рендер шаблона в случае успешной отправки
                return render(request, 'portfolio_app/contact.html', {
                    # Форма не передается (очищается)
                    'form': None,

                    # Флаг успешной отправки
                    'success': True,
                })

            except Exception as e:
                # Обработка исключений при отправке письма

                # Получение полного трейса ошибки
                error_trace = traceback.format_exc()

                # Вывод трейса ошибки в консоль (для отладки)
                print(error_trace)

                # Закомментированный код для создания текстового сообщения об ошибке
                # error_message = f"Ошибка при отправке сообщения: {str(e)}"

            # Рендер шаблона в случае ошибки отправки
            return render(request, 'portfolio_app/contact.html', {
                # Возврат исходной формы
                'form': form,

                # Флаг неудачной отправки
                'success': False
            })


class Custom404View(View):  # Определяем класс представления, наследуя от базового класса View
    def get(self, request, *args,
            **kwargs):  # Метод для обработки GET-запросов; принимает request и любые дополнительные позиционные и именованные аргументы
        # Возвращаем шаблон '404.html' с HTTP-статусом 404
        return render(request, 'portfolio_app/404.html', status=404)


class ProjectCreateView(LoginRequiredMixin,
                        CreateView):  # Определяем класс представления, наследуя от базового класса CreateView
    model = Project  # Указываем модель, с которой будет работать представление
    form_class = ProjectForm  # Указываем форму, которая будет использоваться для создания объекта
    template_name = 'portfolio_app/add_project.html'  # Указываем имя шаблона, который будет использоваться для отображения формы

    login_url = '/login/'  # Закомментированная строка,
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


class ArticleCreateView(LoginRequiredMixin,
                        CreateView):  # Создаем класс ArticleCreateView, наследуя его от CreateView, чтобы реализовать функционал для создания объектов.
    model = Article  # Назначаем модель Article, которую будет использовать это представление для создания объектов.
    form_class = ArticleForm  # Указываем класс формы ArticleForm, которая будет использоваться для ввода данных для нового объекта.
    template_name = 'portfolio_app/add_article.html'  # Указываем путь к HTML-шаблону, который будет отображаться при открытии формы.

    login_url = '/login/'  # Эта строка закомментирована. Она могла бы использоваться,
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
    '''Тестовая функция '''
    # Печать сообщения в консоль для отладки - показывает, что функция вызвана
    print("Функция send_test_email вызвана!")

    try:
        # Отправка электронной почты с помощью встроенной функции Django
        send_mail(
            # Тема письма
            'Бла-бла-бла, я пытаюсь работать.',

            # Текст сообщения
            'Тест сообщение',

            # Email отправителя (должен быть настроен в settings.py)
            'brin14071984@gmail.com',

            # Список получателей (может содержать несколько email)
            ['ascomfort84@gmail.com'],

            # Параметр, который отключает подавление исключений
            # При False будет выброшено подробное исключение в случае ошибки
            fail_silently=False
        )

        # Возвращаем HTTP-ответ об успешной отправке
        return HttpResponse("Письмо отправлено!")

    except Exception as e:
        # Обработка любых исключений, которые могут возникнуть при отправке

        # Печать ошибки в консоль для отладки
        print(f'Ошибка при отправке: {e}')

        # Возвращаем HTTP-ответ с текстом ошибки и статусом 500 (Internal Server Error)
        return HttpResponse(f'Ошибка: {e}', status=500)


class SessionTestView(View):  # Определяем класс SessionTestView, наследующий от базового класса View
    # для обработки HTTP-запросов.
    def get(self, request):  # Определяем метод get, обрабатывающий GET-запросы для данного представления.
        visits = request.session.get('visits', 0)  # Получаем значение ключа 'visits' из сессии пользователя;
        # если ключ не найден, то по умолчанию установим в 0.
        request.session['visits'] = visits + 1  # Увеличиваем значение 'visits' на 1 и записываем его обратно в сессию.
        return HttpResponse(f'Вы посетили эту страницу {visits + 1} раз(а)')  # Возвращаем HTTP-ответ с информацией
        # о количестве посещений страницы.


class SpamProtection:
    @staticmethod
    def check_rate_limit(request):
        '''
        Метод защиты от спама с ограничением количества запросов

        :param request: HTTP-запрос от пользователя
        :return: Boolean - разрешен или заблокирован запрос
        '''
        # Получаем IP-адрес пользователя из метаданных запроса
        user_ip = request.META.get('REMOTE_ADDR')

        # Создаем уникальный ключ кэша для каждого IP-адреса
        cache_key = f'rate_limit: {user_ip}'

        # Получаем количество запросов из кэша, по умолчанию 0
        requests_count = cache.get(cache_key, 0)

        # Если количество запросов >= 2, блокируем дальнейшие запросы
        if requests_count >= 2:
            return False

        # Если это первый запрос, устанавливаем счетчик в кэше на 30 секунд
        if requests_count == 0:
            cache.set(cache_key, 1, timeout=180)
        else:
            # Увеличиваем счетчик запросов на 1
            cache.incr(cache_key, 1)

        # Разрешаем выполнение запроса
        return True
