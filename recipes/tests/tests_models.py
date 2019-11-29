"""
This module tests the models of the faq app
"""

from django.test import TestCase
from recipes.models import *


class TestRecipe(TestCase):
    # This class tests the Tag and TagManager models

    @classmethod
    def setUpTestData(cls):
        # Sets up recipes of all types
        cls.ingredient_typeA = IngredientType.objects.create(name="ITA")
        cls.recipeA = Recipe.objects.create(name="recipeA",
                                            directions="testdirections",
                                            type="F",
                                            )
        cls.recipeB = Recipe.objects.create(name="recipeB",
                                            directions="testdirections",
                                            type="M",
                                            )
        cls.recipeC = Recipe.objects.create(name="recipeC",
                                            directions="testdirections",
                                            type="M",
                                            )
        cls.recipeD = Recipe.objects.create(name="recipeD",
                                            directions="testdirections",
                                            type="D",
                                            )
        cls.recipeE = Recipe.objects.create(name="recipeE",
                                            directions="testdirections",
                                            type="F",
                                            )
        cls.recipeF = Recipe.objects.create(name="recipeF",
                                            directions="testdirections",
                                            type="M",
                                            )
        cls.recipeG = Recipe.objects.create(name="recipeG",
                                            directions="testdirections",
                                            type="M",
                                            )
        cls.recipeH = Recipe.objects.create(name="recipeH",
                                            directions="testdirections",
                                            type="D",
                                            )
        cls.ingredientA = Ingredient.objects.create(name="ingredientA",
                                                    type=cls.ingredient_typeA
                                                    )

    def test_recipe_attributes(self):
        # Tests that recipe instance attributes are of the correct type

        self.assertTrue(isinstance(self.recipeA, Recipe))
        self.assertEqual(type(self.recipeA.name), str)
        self.assertEqual(type(self.recipeA.directions), str)
        self.assertEqual(type(self.recipeA.type), str)

    def test_max_meal_number(self):
        # Tests that the max_meal_number() method of the recipe manager works

        self.assertEqual(Recipe.objects.max_meal_number(3), 2)
        self.assertEqual(Recipe.objects.max_meal_number(1), 1)

    def test_get_remaining_recipes(self):
        """
        Tests that the get_remaining_recipes()
        method of the recipe manager works
        """
        id1 = self.recipeA.id
        id2 = self.recipeE.id
        self.assertEqual(Recipe.objects.get_remaining_recipes("F",[id1]),
                         self.recipeE)
        self.assertEqual(Recipe.objects.get_remaining_recipes("F",[id1, id2]),
                         None)
