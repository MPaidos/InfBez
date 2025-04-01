from django.db import models
from django.contrib.auth.models import AbstractUser

class Tag(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='recipes_images/')


class User(AbstractUser):
    email = models.EmailField()
    role = models.CharField(max_length=50, null=True)
    user_info = models.TextField(null=True, blank=True, )
    image = models.ImageField(upload_to='users_images/', blank=True, null=True)

    def __str__(self):
        return self.username


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    time = models.CharField(max_length=100, null=False)
    difficulty = models.CharField(max_length=150, choices=[('Легкая', 'Легкая'), ('Средняя', 'Средняя'), ('Тяжелая', 'Тяжелая')], null=False)
    rate = models.FloatField(null=True)
    ingredients = models.TextField()
    cooking_steps = models.TextField()
    date_of_addition = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Ужасно'),
        (2, '2 - Плохо'),
        (3, '3 - Нормально'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
    ]
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES, null=False)
    text = models.TextField(null=True, blank=True)
    date_of_addition = models.DateField(auto_now=True)

    def __str__(self):
        return f'Отзыв от {self.user.username} на {self.recipe.title}'

    class Meta:
        unique_together = ('recipe', 'user')

class TagsOfRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    '''class Meta:
        unique_together = (('recipe', 'tag'),)'''


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class RecipeImage(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE) #primary_key=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)


'''class Difficulty(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name'''


