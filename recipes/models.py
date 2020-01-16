"""
recipes/models.py contains the Recipe, Ingredient and IngredientType models.
It also describes the RecipeIngredient association table.
"""
from random import sample

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from fpdf import FPDF

from django.conf import settings


class RecipeManager(models.Manager):
    # Contains the sort_recipes_ingredients() method
    def sort_recipe_ingredients(self, str_array):
        """
        Takes an array of recipe names and returns a dictionary containing
        the ingredients of these recipes (RecipeIngredient objects)
        sorted by ingredient type
        """
        ri_list = []
        for name in str_array:
            recipe = self.get(name=name)
            ri_list.extend(recipe.recipeingredient_set.all())

        sections = {}

        for it in IngredientType.objects.all():
            sections[it.name] = []

        for ri in ri_list:
            sections[ri.ingredient.type.name].append(ri)

        return sections

    def get_remaining_recipes(self, type, ids):
        # Returns all recipes of a given type whose id is not in a list of ids
        same_type_recipes = [recipe.id for recipe in self.filter(type=type)]
        remaining_recipes = list(set(same_type_recipes) - set(ids))
        if remaining_recipes:
            selected_recipe = Recipe.objects.get(
                pk=sample(remaining_recipes, 1)[0])
            return selected_recipe
        else:
            return None

    def stringify_recipe_ingredients(self, recipe):
        """
        Takes a recipe and returns an array of strings describing its
        ingredients with their quantity and unit
        """
        ingredient_list = []
        for ri in recipe.recipeingredient_set.all():
            if ri.quantity:
                ingredient_list.append(
                    "{0} : {1} {2}".format(ri.ingredient.name,
                                           '{0:g}'.format(ri.quantity),
                                           ri.unit
                                           )
                )
            else:
                ingredient_list.append(ri.ingredient.name)

        return ingredient_list

    def max_meal_number(self, absolute_max):
        """
        Returns the lowest number between absolute_max and the number of
        matching recipes for each ingredient type
        """
        max_meal_number = min(
            len(self.filter(type="F")),
            len(self.filter(type="M")),
            len(self.filter(type="D")),
            absolute_max
        )
        return max_meal_number


class RecipeIngredientManager(models.Manager):
    # Contains the aggregate_recipe_ingredients() method
    def aggregate_recipe_ingredients(self, dic):
        """
        Takes a dict where each key is an ingredient type and returns an array
        of RecipeIngredient objects. Returns a dict with similar structure,
        except the arrays contains readable string versions of the recipe
        ingredients. Duplicate ingredients are merged if their unit permits it.
        """
        aggregated_ingredients = {}
        for count, section in enumerate(dic.values()):
            section_ingredients = set([ri.ingredient.name for ri in section])
            section_grocery = []
            for name in section_ingredients:
                matching_ris = [ri for ri in section
                                if ri.ingredient.name == name]
                matching_quantities = [ri.quantity for ri in matching_ris]
                matching_units = [ri.unit for ri in matching_ris]
                if matching_quantities == [None]:
                    section_grocery.append(name)

                elif {"cl", "g", ""} & set(matching_units) == set():
                    section_grocery.append(name)

                else:
                    for unit in ["cl", "g", ""]:
                        if unit in matching_units:
                            quant = sum([ri.quantity for ri in matching_ris
                                      if (ri.unit == unit and ri.quantity)])
                            section_grocery.append(
                                "{0:g}{1} {2}".format(quant, unit, name)
                            )

            aggregated_ingredients[[*dic][count]] = section_grocery

        return aggregated_ingredients


class PDFManager(models.Manager):
    # Contains the create_pdf() method, used to generate grocery list
    def create_pdf(self, dic):
        """
        Takes a dictionnary with arrays of strings as values, creates a pdf out
        of it, then saves and returns the file
        """
        pdf_list = FPDF()
        pdf_list.add_page()
        for key in dic.keys():
            if dic[key]:
                pdf_list.set_font("Arial", size=16)
                pdf_list.cell(200, 15, txt=key, ln=1, align="L")
                pdf_list.set_font("Arial", size=12)
                for grocery in dic[key]:
                    pdf_list.cell(200, 10, txt=grocery, ln=1, align="L")
        path = settings.MEDIA_ROOT + "/grocery.pdf"
        pdf_list.output(path)
        self.all().delete()
        holder = self.create(pdf_file="grocery.pdf")
        file = holder.pdf_file
        return file


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
    ingredients = models.ManyToManyField(Ingredient,
                                         through="RecipeIngredient")
    pdf_file = models.FileField("Fichier PDF",
                                upload_to="recipes_pdfs/",
                                blank=True
                                )
    objects = RecipeManager()

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
    unit = models.CharField("Unité (facultatif)", max_length=30, blank=True)
    objects = RecipeIngredientManager()

    class Meta:
        verbose_name = "association ingrédients-recettes"
        verbose_name_plural = "associations ingrédients-recettes"


class PDFHolder(models.Model):
    # Simply stores a pdf file about to be downloaded
    pdf_file = models.FileField("Fichier PDF",
                                upload_to="test/",
                                blank=True
                                )
    objects = PDFManager()
