"""
The views of the recipes app handle the recipe search engine and the
creation of groceries list.
"""
from random import sample

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from recipes.forms import RecipeSearchForm
from recipes.models import Recipe, IngredientType, PDFHolder, RecipeIngredient

from fpdf import FPDF

from stradacore import settings


def landing(request):
    """
    The landing view displays the home page and search form for the recipes
    app when accessed through GET.
    When using POST through the search form, the view also displays the search
    results.
    """

    context = {
        'form': RecipeSearchForm()
    }

    if request.method == 'POST':
        form = RecipeSearchForm(request.POST)
        if form.is_valid():
            meal_number = int(form.cleaned_data['meal_number'])
            if "F" in form.cleaned_data['course_options']:
                fcs = sample(list(Recipe.objects.filter(type="F")),
                             meal_number)
            if "M" in form.cleaned_data['course_options']:
                mcs = sample(list(Recipe.objects.filter(type="M")),
                             meal_number)
            if "D" in form.cleaned_data['course_options']:
                dts = sample(list(Recipe.objects.filter(type="D")),
                             meal_number)

            meal_list = []
            for x in range(0, meal_number):
                meal = []
                if "fcs" in locals(): meal.append(fcs[x])
                if "mcs" in locals(): meal.append(mcs[x])
                if "dts" in locals(): meal.append(dts[x])
                meal_list.append(meal)

            context['meal_list'] = meal_list

    return render(request, 'recipes/recipes_landing.html', context)


def recipe_download(request, recipe_id):
    # AJAX downloads a recipe's pdf file
    if Recipe.objects.get(id=recipe_id).pdf_file:
        pdf_file = Recipe.objects.get(id=recipe_id).pdf_file
        response = HttpResponse(pdf_file, content_type='text/plain')

        return response


def recipe_refresh(request):
    """
    AJAX sends data about a random recipe of a given type, selected from those
    that has not yet been displayed on the page that sent the request
    """
    if request.method == "POST":
        type = request.POST.get("recipe_type")
        ids = request.POST.get("recipe_ids")
        remaining_recipe = Recipe.objects.get_remaining_recipes(type, ids)

        if not remaining_recipe:
            data = {"status": "out"}
            return JsonResponse(data)

        str_list = Recipe.objects.stringify_recipe_ingredients(remaining_recipe)

        data = {
            "status": "ok",
            "id": remaining_recipe.id,
            "name": remaining_recipe.name,
            "ingredients": str_list,
            "directions": str(remaining_recipe.directions)
        }

        return JsonResponse(data)


def grocery_list(request):
    # AJAX creates a grocery list from given lists of recipes and download it

    if request.method == "POST":
        string_array = request.body.decode("utf-8").split(",")

        srt_ingr = Recipe.objects.sort_recipe_ingredients(string_array)
        agg_ingr = RecipeIngredient.objects.aggregate_recipe_ingredients(srt_ingr)
        file = PDFHolder.objects.create_pdf(agg_ingr)

        response = HttpResponse(file, content_type='application/pdf')
        return response
