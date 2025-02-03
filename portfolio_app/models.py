from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название пректа')  # Название проекта
    description = models.TextField(verbose_name='Описание проекта')  # описание проекта
    link = models.URLField(blank=True, null=True, verbose_name='Ссылка')  # ссылка на проект
    created_at = models.DateTimeField(auto_now_add=True)  # дата создания проекта

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название статьи') # Название статьи
    content = models.TextField(verbose_name='Содержание') # описание статьи
    created_at = models.DateTimeField(auto_now_add=True)  # дата создания статьи

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=100) # имя контакта
    email = models.EmailField() # почта контакта
    message = models.TextField() # сообщение контакта
    created_at = models.DateTimeField(auto_now_add=True) # дата создания контакта

    def __str__(self):
        return f"Сообщение от {self.name}"