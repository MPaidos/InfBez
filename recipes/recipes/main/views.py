from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
import re
from .forms import *

# Create your views here.
def index_page(request):
    return render(request, 'index.html')

def logout_page(request):
    logout(request)
    return redirect('index')

def signup_page(request):
    if request.method == 'POST':
        signupForm = SignupForm(request.POST)
        if signupForm.is_valid():
            newUser = signupForm.save()
            login(request, newUser)
            return redirect('profile')
        else:
            return render(request, 'signup.html', {'signupForm': signupForm})
    else:
        signupForm = SignupForm()
        return render(request, 'signup.html', {'signupForm':signupForm})


def login_page(request):
    loginForm = LoginForm(data=request.POST or None)
    if request.method == "POST":
        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                loginForm.add_error(None, 'Неверное имя пользователя или пароль')
        else:
            loginForm.add_error(None, 'Капча неправильно переписана')
    return render(request, 'login.html', {'loginForm':loginForm})



def recipes_page(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes.html', {'recipes':recipes})


def favorites_page(request):
    return render(request, 'favorites.html')


def profile_page(request):
    user = request.user
    recipes = Recipe.objects.filter(user=user.id)
    return render(request, 'profile.html', {'user': user, 'recipes':recipes})

@login_required
def make_recipe_page(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(False)
            recipe.user = request.user
            recipe.save(True)
            return redirect('index')
        else:
            return HttpResponse('Форма невалидна')
    else:
        form = RecipeForm()
        return render(request, 'makerecipe.html', {'form':form})

def change_user_page(request, id):
    user = User.objects.get(id=id)
    form = ChangeUserForm(instance=user)
    if request.method == "POST":
        form = ChangeUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request, 'changeuser.html', {'form':form})


def about_recipe_page(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    reviews_rating = Review.objects.raw(f'SELECT id, rating FROM main_review WHERE main_review.recipe_id = {id}')
    reviews = recipe.reviews.all().order_by('-date_of_addition')
    total_rate = 0
    total_count = 0

    form = None
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(recipe=recipe, user=request.user).first()
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=user_review) if user_review else ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.recipe = recipe
                review.user = request.user
                review.save()
                for rate in reviews_rating:
                    total_rate += rate.rating
                    total_count += 1
                recipe.rate = round(total_rate / total_count, 1)
                recipe.save(update_fields=['rate'])
                return redirect('about_recipe', id=recipe.id)
        else:
            form = ReviewForm(instance=user_review) if user_review else ReviewForm()

    context = {
        'recipe': recipe,
        'reviews': reviews,
        'form': form,
        'user_review': user_review,
    }
    return render(request, 'aboutrecipe.html', context)

@login_required
def delete_review(request, id):
    review = get_object_or_404(Review, id=id, user=request.user)
    recipe_id = review.recipe.id
    review.delete()
    return redirect('about_recipe', id=recipe_id)


def checkEmail(request):
    data = {}
    emails = User.objects.raw('SELECT email FROM User')
    email = request.POST.get('email')
    isCommonEmail = emails.contains(email)
    result = re.search(r'[\w\._]+@[\w-]+\.[\w]{2,4}', email)
    if not result:
        data = {
            'resultEmail':'Некорректный адрес электронной почты'
        }
    elif isCommonEmail:
        data = {
            'resultEmail':'Такой адрес электронной почты уже существует'
        }
    else:
        pass
    return JsonResponse(data)

def checkPassword(request):
    data = {}
    password = request.POST.get('password1')
    result = re.search(r'[\w\.\!\?\#\%\:]{8,}', password)
    if not result:
        data = {
            'resultPass':'Пароль некорректный. Он должен включать не менее 8 символов (английских, если что)'
        }
    return JsonResponse(data)


def recipe_auth_required(request):
    messages.info(request, "Нам приятно, что вы хотите поделиться своим рецептом на нашем сайте, но для этого вам необходимо авторизоваться или зарегистрироваться.")
    return redirect('login')