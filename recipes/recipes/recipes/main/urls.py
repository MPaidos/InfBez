from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='index'),
    path('register/', views.signup_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('recipes/', views.recipes_page, name='recipes'),
    path('favorites/', views.favorites_page, name='favorites'),
    path('profile/', views.profile_page, name='profile'),
    path('logout/', views.logout_page, name='logout'),
    path('make_recipe/', views.make_recipe_page, name='make_recipe'),
    path('profile/change_user/<int:id>/', views.change_user_page),
    path('recipes/about/<int:id>/', views.about_recipe_page, name='about_recipe'),
    path('check_mail/', views.checkEmail, name='check_mail'),
    path('check_password', views.checkPassword, name='check_password'),
    path('delete_review/<int:id>/', views.delete_review, name='delete_review'),
    path('recipe_auth_required/', views.recipe_auth_required, name='recipe_auth_required'),
    path('profile/change_user/<int:id>/', views.change_user_page, name='change_user'),
]



