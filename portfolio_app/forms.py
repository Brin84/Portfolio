from django import forms
from .models import Project, Article, ContactMessage


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'link']
        # exclude = ['created_at'] # исключает указанные поля
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название'}),
        'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        'link': forms.URLInput(attrs={'class': 'form-control'})}
        # labels = {'title': 'Это название проекта'} # аналог verbose_name

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),}


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}),
        'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),}
