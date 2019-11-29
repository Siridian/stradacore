"""
This module tests the forms of the faq app
"""

from django.test import TestCase
from recipes.forms import *


class TestRecipeSearchForm(TestCase):
    # This class tests the question form

    @classmethod
    def setUpTestData(cls):
        # Sets up recipes to generate form max meal numbers
        Recipe.objects.create(name="F1", type="F")
        Recipe.objects.create(name="F2", type="F")
        Recipe.objects.create(name="F3", type="F")
        Recipe.objects.create(name="M1", type="M")
        Recipe.objects.create(name="M2", type="M")
        Recipe.objects.create(name="M3", type="M")
        Recipe.objects.create(name="D1", type="D")
        Recipe.objects.create(name="D2", type="D")
        Recipe.objects.create(name="D3", type="D")

    def test_form_valid(self):
        # Tests that form is valid with correct data
        data = {"meal_number": "3",
                "course_options": ['F', 'M']
                }
        form = RecipeSearchForm(data=data)
        self.assertTrue((form.is_valid()))

    def test_form_number_out_of_range(self):
        # Tests that form is not valid when meal number is out of range
        data = {"meal_number": "0",
                "course_options": ['F', 'M']
                }
        form = RecipeSearchForm(data=data)
        self.assertFalse((form.is_valid()))

        data = {"meal_number": "4",
                "course_options": ['F', 'M']
                }
        form = RecipeSearchForm(data=data)
        self.assertFalse((form.is_valid()))

    def test_form_incorrect_choices(self):
        # Tests that form is not valid when incorrect choices are sent
        data = {"meal_number": "2",
                "course_options": ['G', 'M']
                }
        form = RecipeSearchForm(data=data)
        self.assertFalse((form.is_valid()))


"""
This module tests the models of the faq app
"""

from django.test import TestCase
from recipes.models import *


class TestRecipe(TestCase):
    # This class tests the Tag and TagManager models

    @classmethod
    def setUpTestData(cls):
        # Sets up three tags
        cls.ingredient_typeA = IngredientType.objects.create(name="ITA")
        cls.recipeA = Recipe.objects.create(name="recipeA",
                                            directions="testdirections",
                                            type="F",
                                            )
        cls.ingredientA = Ingredient.objects.create(name="ingredientA",
                                                    type=cls.ingredient_typeA
                                                    )
        RecipeIngredient.objects.create(recipe=cls.recipeA,
                                        ingredient=cls.ingredientA,
                                        quantity=5,
                                        unit="cl")

    def test_recipe_attributes(self):
        # Tests that recipe instance attributes are of the correct type

        self.assertTrue(isinstance(self.recipeA, Recipe))
        self.assertEqual(type(self.recipeA.name), str)
        self.assertEqual(type(self.recipeA.directions), str)
        self.assertEqual(type(self.recipeA.type), str)
        self.assertEqual(type(self.recipeA.ingredients[0]), Ingredient)


"""
This module tests the views and utils of the faq app
"""
from django.test import TestCase

from recipes.models import *
from recipes.views import *


class TestLanding(TestCase):
    # This class tests the landing view

    @classmethod
    def setUpTestData(cls):
        # Sets up recipes to generate form max meal numbers
        Recipe.objects.create(name="F1", type="F")
        Recipe.objects.create(name="F2", type="F")
        Recipe.objects.create(name="F3", type="F")
        Recipe.objects.create(name="M1", type="M")
        Recipe.objects.create(name="M2", type="M")
        Recipe.objects.create(name="M3", type="M")
        Recipe.objects.create(name="D1", type="D")
        Recipe.objects.create(name="D2", type="D")
        Recipe.objects.create(name="D3", type="D")

    def test_landing_200(self):
        # Tests that landing view returns a 200 code

        response = self.client.get("/recipes/landing/")

        self.assertEqual(response.status_code, 200)

    def test_meal_number_search(self):
        # Tests that the returned meals are of the type specified by the form

        response = self.client.post("/recipes/landing/",
                                    {
                                        'meal_number': '2',
                                        'course_options': ["F"],
                                    }
                                    )
        self.assertEqual(len(response.context["meal_list"]), 2)

    def test_meal_course_number_search(self):
        # Tests that each meal returned contains the correct number of courses
        response = self.client.post("/recipes/landing/",
                                    {
                                        'meal_number': '2',
                                        'course_options': ["F", "M", "D"],
                                    }
                                    )
        self.assertEqual(len(response.context["meal_list"][0]), 3)

    def test_meal_type_search(self):
        # Tests that the returned meals are of the type specified by the form

        response = self.client.post("/recipes/landing/",
                                    {
                                        'meal_number': '2',
                                        'course_options': ["F"],
                                    }
                                    )
        self.assertEqual(response.context["meal_list"][0][0].type, "F")


class TestRecipeDownload(TestCase):
    # This class tests the recipe_download view

    @classmethod
    def setUpTestData(cls):
        # Sets up a recipe and its pdf file
        dic = {"test1": ["test", "test"]}
        cls.file = PDFHolder.objects.create_pdf(dic)
        recipe = Recipe.objects.create(name="testname", pdf_file=cls.file)
        cls.id = recipe.id
        cls.url = "/recipes/recipe_download/" + str(cls.id)

    def test_recipe_download_200(self):
        # Tests that recipe_download view returns a 200 code
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
