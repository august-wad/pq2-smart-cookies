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
    for filename in os.listdir(dirname):
        file_path = join(dirname, filename)
        if isfile(file_path) and filename != ".DS_Store":
            with open(file_path, "r") as file:
                ingredients_strings = [ingredient.strip()
                                       for ingredient in file.readlines()]
                recipe_name = ingredients_strings[0]
                try:
                    recipe_rating = float(ingredients_strings[1].split(' ')[1])
                except ValueError:
                    recipe_rating = -1
                ingredients = [split_ingredient(
                    ingredient_str) for ingredient_str in ingredients_strings[2:]]

                recipes[recipe_name] = [recipe_rating] + ingredients
    return recipes


def split_ingredient(ingredient_str):
    """A helper function to take in a string representing an ingredient,
    and return a list in the format [amount, name]
    parameters:
    ingredient_str: string representing an ingredient from the text files of recipes.
    """
    ingredient_split = [part for part in ingredient_str.split(' ') if part]
    if ingredient_split[1][0] == "(":
        return parse_parenth_unit(ingredient_split)
    elif len(ingredient_split) <= 2 or ingredient_split[1] == 'large':
        return parse_no_unit(ingredient_split)

    ingredient_dict = {"name": '', "unit": '', "amount": 0}
    try:
        ingredient_dict["amount"] = float(ingredient_split[0])
        ingredient_dict["unit"] = ingredient_split[1]
        ingredient_dict["name"] = ' '.join(ingredient_split[2:])

    except ValueError:
        print("could not parse amount and unit from: " +
              ' '.join(ingredient_split))
        ingredient_dict["name"] = ' '.join(ingredient_split)

    return ingredient_dict


def parse_no_unit(ingredient_split):
    ingredient_dict = {"name": '', "unit": '', "amount": 0}
    ingredient_dict["name"] = ' '.join(ingredient_split[1:])
    try:
        ingredient_dict["amount"] = float(ingredient_split[0])

    except ValueError:
        print("could not parse amount and unit from: " +
              ' '.join(ingredient_split))

    if "egg" in ingredient_dict["name"]:
        ingredient_dict["name"] = "egg"
        ingredient_dict["amount"] = ingredient_dict["amount"] * 50
        ingredient_dict["unit"] = "grams"

    return ingredient_dict


def parse_parenth_unit(ingredient_split):
    # like: 1 (18.25 ounce) box red velvet cake mix
    ingredient_dict = {"name": '', "unit": '', "amount": 0}
    ingredient_dict["amount"] = float(ingredient_split[1][1:])
    i = 2
    while ingredient_split[i][-1] != ")":
        ingredient_dict["unit"] = ingredient_dict["unit"] + \
            ingredient_split[i]
        i += 1
    ingredient_dict["unit"] = ingredient_dict["unit"] + \
        ingredient_split[i]
    ingredient_dict["name"] = ' '.join(ingredient_split[i+1:][:-1])

    return ingredient_dict
