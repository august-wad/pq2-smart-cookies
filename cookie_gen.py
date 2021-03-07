import random
import os
import os.path
import join, isfile
import enum

"""
Authors: Danny Little, Bruce Tang, August Wadlington
CSCI 3725
Last Edited: 2021-03-07
"""


class Population:



class Recipe:
    num_of_recipes = 0

    def __init__(self, name, ingredients_list):
        self.name = name
        self.num_of_ingredients = len(ingredients_list)
        Recipe.num_of_recipes += 1
        new_ingredients_list = []
        for ingredient in ingredients_list:
            new_ingredients_list.append(Ingredient(ingredient.amount, ingredient.name))
        self.ingredients_list = new_ingredients_list

    def reproduce_with(self, recipe):
        """TODO"""
    
    def mutate(self, all_ingredients):
        """TODO"""
    
    def normalize(self):
        """TODO"""
    
    def __repr__(self):
        s =


class Ingredient:
    def __init__(self, amount, name):
        self.name
        self.amount
    
    def __repr__(self):
        return f'{self.name}, {self.amount} g'

class Converter:

