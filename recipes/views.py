"""
The views of the recipes app handle the recipe search engine and the
creation of groceries list.
"""

from django.shortcuts import render

from recipes.forms import RecipeSearchForm


def landing(request):
    context = {
        'form': RecipeSearchForm()
    }
    return render(request, 'recipes/recipes_landing.html', context)


def recipes_search(request):
    context = {
        'form': RecipeSearchForm()
    }
    if request.method == 'POST':
        form = RecipeSearchForm(request.POST)
        context = {
            'form': RecipeSearchForm()
        }
        if form.is_valid():
            return render(request, 'recipes/recipes_landing.html', context)
