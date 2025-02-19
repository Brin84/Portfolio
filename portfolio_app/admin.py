from django.contrib import admin
from portfolio_app.models import Project, Article, ContactMessage

admin.site.site_header = 'Панель управления!!!'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'created_at')
    search_fields = ('title',)  # Поиск по названию проекта
    list_filter = ('created_at',)  # Фильтр по дате создания
    ordering = ('-created_at',)  # Сортировка от новых к старым


@admin.register(
    Article)  # Декоратор, регистрирующий модель Article в админ-панели Django, используя класс настройки ArticleAdmin.
class ArticleAdmin(
    admin.ModelAdmin):  # Определяем класс ArticleAdmin, наследуя от admin.ModelAdmin,
    # для настройки отображения модели Article в админке.
    list_display = (
        'title', 'image',
        'created_at')  # Перечисляем поля модели, которые будут отображаться в списке объектов в админке.
    search_fields = ('title', 'content')  # Указываем поля, по которым будет осуществляться поиск в админке.
    list_filter = ('created_at',)  # Указываем поля, по которым можно будет фильтровать объекты в админке.
    ordering = (
        '-created_at',)  # Задаем порядок сортировки объектов в админке, начиная с самых последних по дате создания
    # (обратный порядок).


@admin.register(
    ContactMessage)  # Декоратор регистрирует модель ContactMessage в админ-панели Django
# с использованием класса ContactMessageAdmin.
class ContactMessageAdmin(
    admin.ModelAdmin):  # Определяем класс ContactMessageAdmin, наследуя от admin.ModelAdmin,
    # для настройки отображения модели ContactMessage в админке.
    list_display = (
    'name', 'email', 'created_at',)  # Указываем поля, которые будут отображаться в списке объектов в админке.
    search_fields = ('name', 'email')  # Определяем поля, по которым будет производиться поиск в админке.
    list_filter = ('created_at',)  # Указываем поле, по которому можно фильтровать объекты в админке.
    ordering = (
    '-created_at',)  # Устанавливаем порядок сортировки объектов в админке, начиная с последних по дате создания
    # (в обратном порядке).
