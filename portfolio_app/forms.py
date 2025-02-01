from django import forms
from .models import Project, Article, ContactMessage


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title','description', 'link']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name','email', 'message']

