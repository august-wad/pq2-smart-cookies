import os
from os.path import join, isfile


def main():
    recipes = parse_recipe_files('recipes')
    # iterate through recipe
    for recipe_name in list(recipes.keys()):
        print("Recipe for " + recipe_name + ":")
        ingredients = recipes[recipe_name]

        # iterate through each ingredient in each recipe
        for ingredient in ingredients:
            print(ingredient)


def parse_recipe_files(dirname):
    """A helper function to return a dictionary of 
    recipe information from text files representing each recipe.

    parameters:
    dirname: name of the directory where recipe text files are.
    """
    recipes = {}
    # for filename in os.listdir(dirname):
    for filename in os.listdir(dirname)[:10]:
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
    ingredient_str = ingredient_str.replace('\u2009', ' ')
    ingredient_split = [part for part in ingredient_str.split(' ') if part]
    ingredient_dict = {"name": '', "unit": None, "amount": 0}
    ugly_fractions = {'¼', '½', '¾', '⅐', '⅑', '⅒', '⅓', '⅔',
                      '⅕', '⅖', '⅗', '⅘', '⅙', '⅚', '⅛', '⅜', '⅝', '⅞'}

    # first part is ugly fraction
    if ingredient_split[0] in ugly_fractions:
        ingredient_dict["amount"] += get_annoying_fraction(ingredient_split[0])

        # e.g. ½ egg? I guess?
        if len(ingredient_split) <= 2:
            ingredient_dict["name"] = ' '.join(ingredient_split[1:])

        # e.g. ½ tablespoon sugar
        else:
            ingredient_dict["unit"] = ingredient_split[1]
            ingredient_dict["name"] = ' '.join(ingredient_split[2:])

    else:
        try:
            ingredient_dict["amount"] += float(ingredient_split[0])
        except ValueError:
            print('could not parse:')
            print(ingredient_split)

        # mixed number with ugly fraction, e.g. 1 ½ tablespoons sugar
        if ingredient_split[1] in ugly_fractions:
            ingredient_dict["amount"] += get_annoying_fraction(
                ingredient_split[1])
            ingredient_split.pop(1)

        # unit like "1 apple" or "1 large egg"
        if len(ingredient_split) <= 2 or ingredient_split[1] == 'large':
            ingredient_dict["amount"] = float(ingredient_split[0])
            ingredient_dict["name"] = ' '.join(ingredient_split[1:])
            if ingredient_dict["name"] == "egg" or ingredient_dict["name"] == "eggs":
                ingredient_dict["amount"] = ingredient_dict["amount"] * 50
                ingredient_dict["unit"] = "grams"

        else:
            ingredient_dict["unit"] = ingredient_split[1]
            ingredient_dict["name"] = ' '.join(ingredient_split[2:])

    ingredient_dict["amount"] = round(ingredient_dict["amount"], 4)
    return ingredient_dict


def get_annoying_fraction(fraction):
    return {'¼': 1/4, '½': .5, '¾': 3/4, '⅐': 1/7, '⅑': 1/9, '⅒': .1, '⅓': 1/3, '⅔': 2/3, '⅕': .2, '⅖': .4, '⅗': .6, '⅘': .8, '⅙': 1/6, '⅚': 5/6, '⅛': 1/8, '⅜': 3/8, '⅝': 5/8, '⅞': 7/8}.get(fraction)


main()
