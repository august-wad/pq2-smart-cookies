import random
from os import *
from os.path import isfile

from clean_text import get_recipe_dict

"""
Authors: Danny Little, Bruce Tang, August Wadlington
CSCI 3725
Last Edited: 2021-03-10
"""


class Population:
    def __init__(self, recipes_list):
        """Represents a population of recipes, from which the parents of each generation are chosen.
        parameters:
        recipes_list: a list of already instantiated recipe objects that will make up the initial population.
        """
        self.recipes_list = recipes_list
        self.all_ingredients = []
        self.all_ingredient_objects = {}
        for recipe in self.recipes_list:
            for ingredient in recipe.ingredients_list:
                if (ingredient.name not in self.all_ingredients):
                    self.all_ingredients.append(ingredient.name)

                if ingredient.name in self.all_ingredient_objects:
                    self.all_ingredient_objects[ingredient.name].append(
                        ingredient)
                else:
                    self.all_ingredient_objects.update(
                        {ingredient.name: [ingredient]})

    def freq_ingredients(self):
        freqency_map = {}
        for recipe in self.recipes_list:
            for ingredient in recipe.ingredients_list:
                if ingredient.name in freqency_map:
                    freqency_map[ingredient.name] += 1
                else:
                    freqency_map.update({ingredient.name: 1})
        return freqency_map

    def generate(self):
        freqency_map = self.freq_ingredients()
        self.all_ingredients.sort(
            key=lambda ingredient: freqency_map.get(ingredient), reverse=True)
        core = self.all_ingredients[:round(len(self.all_ingredients) * 0.05)]
        extra = list(set(self.all_ingredients) - set(core))
        output_ingredient_list = []

        for ingredient_name in core:
            ingredient_objects = self.all_ingredient_objects.get(
                ingredient_name)
            high = max(
                ingredient.amount for ingredient in ingredient_objects)
            low = min(
                ingredient.amount for ingredient in ingredient_objects)
            new_amount = random.uniform(low, high)
            output_ingredient_list.append(
                Ingredient(ingredient_name, new_amount))

        i = 3
        while i > 0:
            extra_ingredient_name = random.choice(extra)
            extra.remove(extra_ingredient_name)
            extra_objects = self.all_ingredient_objects.get(
                extra_ingredient_name)
            extra_amount = random.choice(extra_objects)
            output_ingredient_list.append(
                Ingredient(extra_ingredient_name, extra_amount.amount))
            i -= 1

        return output_ingredient_list


class Recipe:
    num_of_recipes = 0

    def __init__(self, name, ingredients_list):
        self.name = name
        self.num_of_ingredients = len(ingredients_list)
        Recipe.num_of_recipes += 1
        new_ingredients_list = []
        for ingredient in ingredients_list:
            new_ingredients_list.append(Ingredient(
                ingredient.name, ingredient.amount))
        self.ingredients_list = new_ingredients_list

    def normalize(self):
        """This method finds the percentage off from 100 oz the recipe's sum of ingredients is,
            then corrects to that amount by multiplying every ingredient amount by that ratio
        """
        total = sum(ingredients.amount for ingredients in self.ingredients_list)
        scaling_factor = 1000 / total
        for ingredient in self.ingredients_list:
            ingredient.amount *= scaling_factor
            ingredient.amount = round(ingredient.amount, 3)

    def __repr__(self):
        s = 'Recipe for ' + self.name + ':\n'
        for i in self.ingredients_list:
            s += '\t' + i.__repr__() + '\n'
        return s


class Ingredient:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def __repr__(self):
        return f'{self.name}, {self.amount}'


def cup_to_g(name, amount):
    storage = amount / .25
    if name == "flour":
        amount = storage * 32
    elif name == "butter":
        amount = storage * 57
    elif name == "white sugar":
        amount = storage * 50
    elif name == "brown sugar":
        amount = storage * 45
    elif name == "icing sugar":
        amount = storage * 35
    elif name == "water":
        amount = storage * 60
    elif name == "cornstarch":
        amount = storage * 30
    elif name == "milk":
        amount = storage * 60
    elif name == "chocolate chips":
        amount = storage * 45
    elif name == "baking soda":
        amount = storage * 72
    elif name == "salt":
        amount = storage * 72
    elif name == "baking powder":
        amount = storage * 60
    elif name == "all-purpose flour":
        amount = storage * 32
    elif name == "vanilla extract" or name == "vanilla":
        amount = storage * 60
    else:
        amount = storage * 25

    return amount


def tspoon_to_cup(amount):
    return amount * .0208


def tbspoon_to_cup(amount):
    return amount * .0625


def translate(recipe_dict):
    recipe_list = []
    for key in list(recipe_dict.keys()):
        parse_store = recipe_dict.get(key)
        ingredients_list = []
        for ingredient in parse_store:
            if ingredient.get("unit") == "teaspoons" or ingredient.get("unit") == "teaspoon":
                cup_from_tspoon = tspoon_to_cup(ingredient.get("amount"))
                ingredient.update({"amount": cup_from_tspoon})
                ingredient.update({"unit": "cups"})
            if ingredient.get("unit") == "tablespoon" or ingredient.get("unit") == "tablespoons":
                cup_from_tbspoon = tbspoon_to_cup(ingredient.get("amount"))
                ingredient.update({"amount": cup_from_tbspoon})
                ingredient.update({"unit": "cups"})
            if ingredient.get("unit") == "cup" or ingredient.get("unit") == "cups":
                grams_from_cups = cup_to_g(ingredient.get(
                    "name"), ingredient.get("amount"))
                ingredient.update({"amount": grams_from_cups})
                ingredient.update({"unit": "grams"})

            ingredients_list.append(Ingredient(
                ingredient.get("name"), ingredient.get("amount")))
        recipe_list.append(Recipe(key, ingredients_list))
    return recipe_list


def main():
    recipe_dict = get_recipe_dict()
    recipe_list = translate(recipe_dict)
    p = Population(recipe_list)
    output_recipe = p.generate()
    output_name = "Demo 1"
    recipe = Recipe(output_name, output_recipe)
    recipe.normalize()
    print(recipe)


main()
