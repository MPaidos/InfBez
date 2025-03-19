from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import *

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class SignupForm(UserCreationForm):
    email = forms.EmailField()
    '''user_info = forms.CharField(widget=forms.Textarea, required=False)
    image = forms.ImageField(required=False)'''
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

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

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

class RecipeImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'

class TagsOfRecipeForm(forms.ModelForm):
    class Meta:
        model = TagsOfRecipe
        fields = '__all__'

class ChangeUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'user_info',
            'image'
        ]