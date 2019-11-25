"""
recipes/admin.py registers the Recipe, Ingredient and IngredientType models,
and adds Ingredients as Recipe inlines
"""


from django.contrib import admin

from recipes.models import IngredientType, Ingredient, Recipe, RecipeIngredient

admin.site.register(IngredientType)
admin.site.register(Ingredient)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = ('name', 'directions', 'type')
    inlines = (RecipeIngredientInline,)

