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


class TestRecipeRefresh(TestCase):
    # This class tests the recipe_download view

    def test_recipe_refresh_200(self):
        # Tests that recipe_download view returns a 200 code
        response = self.client.post("/recipes/recipe_refresh/",
                                    {
                                        'recipe_type': 'F',
                                        'recipe_ids': [3],
                                    })

        self.assertEqual(response.status_code, 200)

