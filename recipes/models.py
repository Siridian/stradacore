from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


class IngredientType(models.Model):
    name = models.TextField("type", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "type d'ingrédient"
        verbose_name_plural = "types d'ingrédient"


class Ingredient(models.Model):
    name = models.CharField(
        "Nom de l'ingrédient",
        max_length=50,
        unique=True
    )
    unit = models.CharField("Unité (facultatif)", max_length=30,  blank=True)
    type = models.ForeignKey(IngredientType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ingrédient"
        verbose_name_plural = "ingrédients"


class Recipe(models.Model):
    FIRST_COURSE = "F"
    MAIN_COURSE = "M"
    DESSERT = "D"
    RECIPE_TYPE_CHOICES = [
        (FIRST_COURSE, 'Entrée'),
        (MAIN_COURSE, 'Plat principal'),
        (DESSERT, 'Dessert'),
    ]
    name = models.CharField(
        "Nom de la recette",
        max_length=100,
        unique=True
    )
    directions = RichTextUploadingField("Instructions", blank=True)
    type = models.CharField(
        max_length=1,
        choices=RECIPE_TYPE_CHOICES,
        default=MAIN_COURSE,
    )
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "recette"
        verbose_name_plural = "recettes"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField("Quantité", blank=True, null=True)

    class Meta:
        verbose_name = "association ingrédients-recettes"
        verbose_name_plural = "associations ingrédients-recettes"
