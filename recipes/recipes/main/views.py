from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
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
                return HttpResponse("Не нашлось пользователя. Мб неправильный логин или пароль")
        else:
            return HttpResponse("форма невалидна")
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
    pass