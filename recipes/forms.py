"""
Contains the recipes app's forms, such as the recipe search form,
used by the users to find meals and recipes matching their own criteria
"""

from django import forms


class RecipeSearchForm(forms.Form):
    """
    The recipe search form is used in the recipes app main feature.
    It must contain a number of meal to produce (between 1 and 7),
    and between one and three course options
    """
    _meal_choices = [(x, x) for x in range(1, 8)]
    _course_choices = (
        ("F", "Entrée"),
        ("M", "Plat Principal"),
        ("D", "Dessert"),
    )
    range = [(1, 1), (2, 2)]
    meal_number = forms.ChoiceField(choices=_meal_choices)
    course_options = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=_course_choices
    )

    def clean_course_options(self):
        # Makes sure at least one course option has been selected
        data = self.cleaned_data['course_options']
        print("alertdata")
        print(data)
        if not data:
            raise forms.ValidationError("Au moins un type de plat doit être présent !")

        return data
