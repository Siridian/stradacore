"""
recipes/models.py contains the Recipe, Ingredient and IngredientType models.
It also describes the RecipeIngredient association table.
"""

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


class IngredientType(models.Model):
    """
    A simple string to name an ingredient category,
    later referenced in the Ingredient model
    """
    name = models.TextField("type", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "type d'ingrédient"
        verbose_name_plural = "types d'ingrédient"


class Ingredient(models.Model):
    """
    The Ingredient model stores a name, unit and type as an ingredient
    usable in the Recipe model
    """
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
    """
    The Recipe model is key to the recipes app core feature.
    It contains the name (string), directions (ckeditor upload field) and type
    (one among three choices) and ingredients (through the RecipeIngredient
    custom association table) of a recipe.
    """
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
    pdf_file = models.FileField("Fichier PDF",
                                upload_to="recipes_pdfs/",
                                blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "recette"
        verbose_name_plural = "recettes"


class RecipeIngredient(models.Model):
    """
    This model is a custom association table between Recipe and Ingredient,
    that allows to store a specific quantity for each single association
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField("Quantité", blank=True, null=True)

    class Meta:
        verbose_name = "association ingrédients-recettes"
        verbose_name_plural = "associations ingrédients-recettes"
