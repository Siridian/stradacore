from django.contrib import admin

from recipes.models import IngredientType, RecipeType, Ingredient, Recipe, RecipeIngredient

admin.site.register(IngredientType)
admin.site.register(RecipeType)
admin.site.register(Ingredient)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = ('name', 'directions', 'type')
    inlines = (RecipeIngredientInline,)

