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
        Recipe.objects.create(name="F1", type = "F")
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

    def test_form_incorrect_choices(self):
        # Tests that form is not valid when incorrect choices are sent
        data = {"meal_number": "2",
                "course_options": ['G', 'M']
                }
        form = RecipeSearchForm(data=data)
        self.assertFalse((form.is_valid()))


