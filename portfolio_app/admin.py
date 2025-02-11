from django.contrib import admin
from portfolio_app.models import Project, Article, ContactMessage

admin.site.site_header = 'Панель управления!!!'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'created_at')
    search_fields = ('title',)  # Поиск по названию проекта
    list_filter = ('created_at',)  # Фильтр по дате создания
    ordering = ('-created_at',)  # Сортировка от новых к старым


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at',)
    search_fields = ('name', 'email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
