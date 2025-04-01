from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import *


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    captcha = CaptchaField(label='Введите текст с картинки')


class SignupForm(UserCreationForm):
    email = forms.EmailField(label='Электронная почта')
    captcha = CaptchaField(label='Введите текст с картинки')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с такой почтой уже есть")
        return email


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'time',
            'difficulty',
            'ingredients',
            'cooking_steps'
        ]
        labels = {
            'title': 'Название рецепта',
            'description': 'Описание рецепта',
            'time': 'Время приготовления',
            'difficulty': 'Сложность',
            'ingredients': 'Ингредиенты',
            'cooking_steps': 'Этапы приготовления',
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'
        labels = {
            'name': 'Название тега',
        }


class RecipeImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = '__all__'
        labels = {
            'image': 'Изображение',
        }


'''class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
        labels = {
            'content': 'Текст отзыва',
            'rating': 'Оценка',
        }'''


class TagsOfRecipeForm(forms.ModelForm):
    class Meta:
        model = TagsOfRecipe
        fields = '__all__'
        labels = {
            'tag': 'Тег',
        }


class ChangeUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'user_info',
            'image'
        ]
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
            'user_info': 'Информация о пользователе',
            'image': 'Изображение профиля',
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        labels = {
            'rating': 'Оценка',
            'text': 'Комментарий',
        }
        widgets = {
            'rating': forms.RadioSelect(choices=Review.RATING_CHOICES),
            'text': forms.Textarea(attrs={'rows': 4}),
        }
