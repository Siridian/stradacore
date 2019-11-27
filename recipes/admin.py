"""
recipes/admin.py registers the Recipe, Ingredient and IngredientType models,
and adds Ingredients as Recipe inlines
"""


from django.contrib import admin

from recipes.models import IngredientType, Ingredient, Recipe, RecipeIngredient

admin.site.register(IngredientType)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ['name']
    radio_fields = {"type": admin.VERTICAL}


class RecipeIngredientInline(admin.TabularInline):
    autocomplete_fields = ['ingredient']
    fields = ['ingredient', 'quantity', 'unit']
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = ('name', 'directions', 'type', 'pdf_file')
    radio_fields = {"type": admin.VERTICAL}
    inlines = (RecipeIngredientInline,)

