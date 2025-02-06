from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название проекта')  # Название проекта
    description = models.TextField(verbose_name='Описание проекта')  # описание проекта
    link = models.URLField(blank=True, null=True, verbose_name='Ссылка')  # ссылка на проект
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')  # дата создания проекта

    class Meta:
        verbose_name = 'проект'
        verbose_name_plural = 'Проекты'



    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название статьи')  # Название статьи
    content = models.TextField(verbose_name='Содержание')  # описание статьи
    created_at = models.DateTimeField(auto_now_add=True)  # дата создания статьи


    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)  # имя контакта
    email = models.EmailField()  # почта контакта
    message = models.TextField()  # сообщение контакта
    created_at = models.DateTimeField(auto_now_add=True)  # дата создания контакта


    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f"Сообщение от {self.name}"
