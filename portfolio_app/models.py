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

    def str(self):
        return f"Сообщение от {self.name}"