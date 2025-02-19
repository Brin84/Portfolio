from django import forms
from .models import Project, Article, ContactMessage


class ProjectForm(forms.ModelForm):  # Определяем класс формы ProjectForm, который наследует от forms.ModelForm.
    class Meta:  # Внутренний класс Meta используется для определения метаданных для формы.
        model = Project  # Указываем, что форма связана с моделью Project.
        fields = ['title', 'description', 'link']  # Указываем поля модели, которые будут включены в форму.
        # exclude = ['created_at']  # Исключает указанные поля из формы (строка закомментирована).

        widgets = {  # Определяем виджеты для отображения полей формы.
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название'}),
            # Настраиваем TextInput для поля 'title' с классом и placeholder.
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            # Настраиваем Textarea для поля 'description' с классом и количеством строк.
            'link': forms.URLInput(attrs={'class': 'form-control'})  # Настраиваем URLInput для поля 'link' с классом.
        }

        # labels = {'title': 'Это название проекта'}  # Устанавливает пользовательскую метку для поля 'title',
        # аналогично verbose_name (строка закомментирована).


class ArticleForm(forms.ModelForm):  # Определяем класс формы ArticleForm, наследующий от forms.ModelForm.
    class Meta:  # Внутренний класс Meta используется для указания метаданных формы.
        model = Article  # Указываем, что форма связана с моделью Article.
        fields = ['title', 'content']  # Определяем, какие поля модели будут включены в форму.

        widgets = {  # Словарь widgets используется для настройки отображения полей формы.
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название'}),
            # Настраиваем TextInput для поля 'title' с классом Bootstrap и подсказкой.
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            # Настраиваем Textarea для поля 'content' с классом Bootstrap и количеством строк.
        }


class ContactForm(forms.ModelForm):  # Определяем класс формы ContactForm, который наследует от forms.ModelForm.
    class Meta:  # Внутренний класс Meta используется для указания метаданных формы.
        model = ContactMessage  # Указываем, что форма связана с моделью ContactMessage.
        fields = ['name', 'email', 'message']  # Определяем, какие поля модели будут включены в форму.

        widgets = {  # Словарь widgets используется для настройки отображения полей формы.
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}),
            # Настраиваем TextInput для поля 'name' с классом Bootstrap и подсказкой.
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            # Настраиваем Textarea для поля 'message' с классом Bootstrap и количеством строк.
        }


class SearchForm(forms.Form):  # Определяем класс формы SearchForm, который наследует от forms.Form.
    query = forms.CharField(  # Определяем поле формы с именем 'query' типа CharField.
        max_length=250,  # Устанавливаем максимальную длину вводимого текста в 250 символов.
        required=False,  # Указываем, что поле не является обязательным для заполнения.
        label='Поиск',  # Устанавливаем метку для поля, которая будет отображаться на форме.
        widget=forms.TextInput(attrs={  # Настраиваем виджет TextInput для поля.
            'class': 'form-control',  # Применяем класс Bootstrap для стилизации элемента ввода.
            'placeholder': 'Поиск'  # Устанавливаем текст подсказки, который будет отображаться в пустом поле.
        })
    )
