import os
from os.path import join, isfile


def get_recipe_dict():
    return parse_recipe_files('recipes')


def parse_recipe_files(dirname):
    """A helper function to return a dictionary of 
    recipe information from text files representing each recipe.

    parameters:
    dirname: name of the directory where recipe text files are.
    """
    recipes = {}
    # for filename in os.listdir(dirname):
    for filename in os.listdir(dirname):
        file_path = join(dirname, filename)
        if isfile(file_path) and filename != ".DS_Store":
            with open(file_path, "r") as file:
                ingredients_strings = [ingredient.strip()
                                       for ingredient in file.readlines()]
                ingredients = [split_ingredient(
                    ingredient_str) for ingredient_str in ingredients_strings[1:]]

                # store in dictionary without .txt
                recipes[filename.split('.')[0]] = ingredients
    return recipes


def split_ingredient(ingredient_str):
    """A helper function to take in a string representing an ingredient,
    and return a list in the format [amount, name]
    parameters:
    ingredient_str: string representing an ingredient from the text files of recipes.
    """
    ingredient_split = [part for part in ingredient_str.split(' ') if part]
    ingredient_dict = {"name": '', "unit": None, "amount": 0}
    try:
        # parse amount
        ingredient_dict["amount"] = float(ingredient_split[0])

        # if unit not given
        if len(ingredient_split) <= 2 or ingredient_split[1] == 'large':
            ingredient_dict["name"] = ' '.join(ingredient_split[1:])
            if ingredient_dict["name"] == "egg" or ingredient_dict["name"] == "eggs":
                ingredient_dict["amount"] = ingredient_dict["amount"] * 50
                ingredient_dict["unit"] = "grams"
        # unit and name given
        else:
            ingredient_dict["unit"] = ingredient_split[1]
            ingredient_dict["name"] = ' '.join(ingredient_split[2:])
    except ValueError:
        print("could not parse amount and unit from: " +
              ' '.join(ingredient_split))
        ingredient_dict["name"] = ' '.join(ingredient_split)

    return ingredient_dict
