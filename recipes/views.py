"""
The views of the recipes app handle the recipe search engine and the
creation of groceries list.
"""
from random import sample

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from recipes.forms import RecipeSearchForm
from recipes.models import Recipe


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
        file_name = pdf_file.name.split('/')[-1]
        response = HttpResponse(pdf_file, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % file_name
        print(file_name)

        return response


def recipe_refresh(request):
    #
    if request.method == "POST":
        recipe_type = request.POST.get("recipe_type")
        recipe_ids = request.POST.get("recipe_ids")

        same_type_recipes = [recipe.id
                             for recipe
                             in Recipe.objects.filter(type=recipe_type)
                             ]
        recipe_ids_int = (int(n) for n in recipe_ids.split())
        remaining_recipes = list(set(same_type_recipes) - set(recipe_ids_int))
        if not remaining_recipes:
            data = {"status": "out"}
            return JsonResponse(data)

        selected_recipe = Recipe.objects.get(pk=sample(remaining_recipes, 1)[0])
        ingredient_list = []
        for ri in selected_recipe.recipeingredient_set.all():
            if ri.quantity:
                ingredient_list.append("{0} : {1} {2}".format(ri.ingredient.name,
                                                              '{0:g}'.format(ri.quantity),
                                                              ri.ingredient.unit
                                                              )
                                       )
            else:
                ingredient_list.append(ri.ingredient.name)
        data = {
            "status": "ok",
            "id": selected_recipe.id,
            "name": selected_recipe.name,
            "ingredients": ingredient_list,
            "directions": str(selected_recipe.directions)
        }

        return JsonResponse(data)
