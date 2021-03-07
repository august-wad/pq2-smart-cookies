import random
import os
import os.path
import join
import isfile
import enum

"""
Authors: Danny Little, Bruce Tang, August Wadlington
CSCI 3725
Last Edited: 2021-03-07
"""


class Population:
    def __init__(self, recipes_list):
        """Represents a population of recipes, from which the parents of each generation are chosen.
        parameters:
        recipes_list: a list of already instantiated recipe objects that will make up the initial population.
        """
        self.recipes_list = recipes_list
        self.all_ingredients = set()
        for recipe in self.recipes_list:
            for ingredient in recipe.ingredients_list:
                self.all_ingredients.add(ingredient.name)

    def freq_ingredients(recipes_list):
        freqency_map = {}
        for recipe in recipes_list:
            for ingredient in recipe:
                if ingredient.name in freqency_map:
                    freqency_map[ingredient.name] += 1
                else:
                    freqency_map.update({ingredient.name: 1})
        return freqency_map


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

    def reproduce_with(self, recipe):
        """TODO"""

    def mutate(self, all_ingredients):
        """TODO"""

    def normalize(self):
        """TODO"""

    def __repr__(self):
        s = 'Recipe for ' + self.name + ':\n'
        for i in self.ingredients_list:
            s += '\t' + i.__repr() + '\n'
        return s

class Ingredient:
    def __init__(self, amount, name):
        self.name
        self.amount

    def __repr__(self):
        return f'{self.name}, {self.amount} g'


class Converter:
