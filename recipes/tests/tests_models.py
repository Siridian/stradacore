"""
This module tests the models of the faq app
"""

from django.test import TestCase
from recipes.models import *


class TestManagers(TestCase):
    # This class tests the managers of the recipes models

    @classmethod
    def setUpTestData(cls):
        # Sets up recipes of all types
        cls.ingredient_typeA = IngredientType.objects.create(name="ITA")
        cls.ingredient_typeB = IngredientType.objects.create(name="ITB")

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
        cls.ingredientB = Ingredient.objects.create(name="ingredientB",
                                                    type=cls.ingredient_typeB
                                                    )
        cls.ingredientC = Ingredient.objects.create(name="ingredientC",
                                                    type=cls.ingredient_typeA
                                                    )
        cls.ingredientD = Ingredient.objects.create(name="ingredientD",
                                                    type=cls.ingredient_typeB
                                                    )
        cls.riA = RecipeIngredient.objects.create(recipe=cls.recipeA,
                                                  ingredient=cls.ingredientA,
                                                  quantity=5,
                                                  unit="cl"
                                                  )
        cls.riB = RecipeIngredient.objects.create(recipe=cls.recipeB,
                                                  ingredient=cls.ingredientB,
                                                  quantity=5,
                                                  unit="g"
                                                  )
        cls.riC = RecipeIngredient.objects.create(recipe=cls.recipeA,
                                                  ingredient=cls.ingredientC
                                                  )
        cls.riD = RecipeIngredient.objects.create(recipe=cls.recipeB,
                                                  ingredient=cls.ingredientD,
                                                  quantity=5
                                                  )

    def test_sort_recipe_ingredients(self):
        # Tests the sort_recipe_ingredients() method of the recipe manager
        str_arr = ["recipeA", "recipeB", "recipeC", "recipeD"]
        dic = Recipe.objects.sort_recipe_ingredients(str_arr)

        self.assertEqual(len(dic.keys()), 2)
        self.assertEqual(dic["ITA"], [self.riA, self.riC])
        self.assertEqual(dic["ITB"], [self.riB, self.riD])

    def test_get_remaining_recipes(self):
        # Tests the get_remaining_recipes() method of the recipe manager
        id1 = self.recipeA.id
        id2 = self.recipeE.id
        self.assertEqual(Recipe.objects.get_remaining_recipes("F", [id1]),
                         self.recipeE)
        self.assertEqual(Recipe.objects.get_remaining_recipes("F", [id1, id2]),
                         None)

    def test_stringify_recipe_ingredients(self):
        # Tests the stringify_recipe_ingredients() method of the recipe manager
        str_arr = Recipe.objects.stringify_recipe_ingredients(self.recipeA)

        self.assertEqual(str_arr[0], "ingredientA : 5 cl")
        self.assertEqual(str_arr[1], "ingredientC")

    def test_max_meal_number(self):
        # Tests the max_meal_number() method of the recipe manager
        self.assertEqual(Recipe.objects.max_meal_number(3), 2)
        self.assertEqual(Recipe.objects.max_meal_number(1), 1)

    def test_aggregate_recipe_ingredients(self):
        """
        Tests the aggregate_recipe_ingredients() method of the recipe manager
        """
        dic = {
            "ITA": [self.riA, self.riB],
            "ITB": [self.riC, self.riD],
        }
        new_dic = RecipeIngredient.objects.aggregate_recipe_ingredients(dic)
        for key in new_dic:
            print(new_dic[key])
        self.assertEqual(len(new_dic.keys()), 2)
        self.assertTrue("5cl ingredientA" in new_dic["ITA"])
        self.assertTrue("5g ingredientB" in new_dic["ITA"])
        self.assertTrue("ingredientC" in new_dic["ITB"])
        self.assertTrue("5 ingredientD" in new_dic["ITB"])
