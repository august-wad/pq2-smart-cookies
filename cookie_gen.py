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
        self.ingredients_list = ingredients_list
        self.name = name
        self.num_of_ingredients = len(ingredients_list)
        Recipe.num_of_recipes += 1


class Ingredient:
    def __init__(self, amount, name):
        self.name
        self.amount
    
    def __repr__(self):
        return f'{self.name}, {self.amount} g'

class Converter:
    
