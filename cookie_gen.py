import random
from os import *
from os.path import isfile
import enum
import pint

from clean_text import get_recipe_dict


"""
Authors: Danny Little, Bruce Tang, August Wadlington
CSCI 3725
Last Edited: 2021-03-09
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
                self.all_ingredients.add(ingredient.name)

                if ingredient.name in self.all_ingredient_objects:
                    self.all_ingredient_objects[ingredient.name].add(
                        ingredient)
                else:
                    self.all_ingredient_objects.update(
                        {ingredient.name: [ingredient]})

    def freq_ingredients(self):
        freqency_map = {}
        for recipe in self.recipes_list:
            for ingredient in recipe:
                if ingredient.name in freqency_map:
                    freqency_map[ingredient.name] += 1
                else:
                    freqency_map.update({ingredient.name: 1})
        return freqency_map

    def generate(self, freqency_map):
        self.all_ingredients.sort(
            key=lambda ingredient: freqency_map.get(ingredient.name), reverse=True)
        core = self.all_ingredients[:len(self.all_ingredients) * 0.6]
        extra = list(set(self.all_ingredients) - set(core))

        # categorize ingreidents into core and extra
        # cutoff for the core ingredients is set to top 60% for now
        # output a combination of core plus random extras


class Recipe:
    num_of_recipes = 0

    def __init__(self, name, ingredients_list):
        self.name = name
        self.num_of_ingredients = len(ingredients_list)
        Recipe.num_of_recipes += 1
        new_ingredients_list = []
        for ingredient in ingredients_list:
            new_ingredients_list.append(Ingredient(
                ingredient.amount, ingredient.name))
        self.ingredients_list = new_ingredients_list

    def __repr__(self):
        s = 'Recipe for ' + self.name + ':\n'
        for i in self.ingredients_list:
            s += '\t' + i.__repr__() + '\n'
        return s


class Ingredient:
    def __init__(self, amount, name):
        self.name = name
        self.amount = amount

    def __repr__(self):
        return f'{self.name}, {self.amount} g'


def cup_to_g(name, amount):
    storage = amount / .25
    if (name == "flour"):
        amount = storage * 32
    elif (name == "butter"):
        amount = storage * 57
    elif (name == "sugar"):
        amount = storage * 50
    elif (name == "brown sugar"):
        amount = storage * 45
    elif (name == "water"):
        amount = storage * 60
    elif (name == "cornstarch"):
        amount = storage * 30
    elif (name == "milk"):
        amount = storage * 60
    elif (name == "chocolate chips"):
        amount = storage * 45
    elif (name == "baking soda"):
        amount = storage * 72
    elif (name == "salt"):
        amount = storage * 72
    elif (name == "baking powder"):
        amount = storage * 60

    return amount


def tspoon_to_cup(amount):
    return amount * .0208


def tbspoon_to_cup(amount):
    return amount * .0625


def main():
    recipe_dict = get_recipe_dict()


main()
