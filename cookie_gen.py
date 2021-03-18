"""
Authors: Danny Little, Bruce Tang, August Wadlington
CSCI 3725
Last Edited: 2021-03-17
"""

import random
from math import log10
from os import *
from os.path import isfile
from clean_text import get_recipe_dict


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

    def generate(self, num_core, num_extras):
        freqency_map = self.freq_ingredients()
        output_ingredient_list = []
        self.all_ingredients.sort(
            key=lambda ingredient: freqency_map.get(ingredient), reverse=True)
        core = self.all_ingredients[:num_core]
        core_ingredients = set()

        # select 10 core ingredients probabilistically from top num_core ingredients
        recipe_freq = [freqency_map.get(recipe)
                       for recipe in self.recipes_list]
        while len(core_ingredients) < Recipe.NUM_CORE:
            ingredient = random.choices(core, weights=recipe_freq)
            while ingredient in core_ingredients:
                ingredient = random.choices(core, weights=recipe_freq)
            ingredient_objects = self.all_ingredient_objects.get(ingredient)
            high = max(
                i.amount for i in ingredient_objects)
            low = min(
                i.amount for i in ingredient_objects)
            new_amount = random.uniform(low, high)
            output_ingredient_list.append(
                Ingredient(ingredient, new_amount))

        # and the rest is the extra pool
        extra = list(set(self.all_ingredients) - core_ingredients)
        i = num_extras
        while i > 0:
            extra_ingredient_name = random.choice(extra)
            extra.remove(extra_ingredient_name)
            extra_objects = self.all_ingredient_objects.get(
                extra_ingredient_name)
            extra_amount = random.choice(extra_objects)
            output_ingredient_list.append(
                Ingredient(extra_ingredient_name, extra_amount.amount))
            i -= 1

        return GeneratedRecipe(f"New recipe", output_ingredient_list)


class Recipe:
    NUM_CORE = 10

    def __init__(self, name, ingredients_list, rating=None):
        self.name = name
        self.rating = rating
        self.num_of_ingredients = len(ingredients_list)
        new_ingredients_list = []
        for ingredient in ingredients_list:
            new_ingredients_list.append(Ingredient(
                ingredient.name, ingredient.amount))
        self.ingredients_list = new_ingredients_list
        self.normalize()

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
        s = f'Recipe for {self.name}:\n'
        for i in self.ingredients_list:
            s += '\t' + i.__repr__() + '\n'
        return s


class GeneratedRecipe(Recipe):
    def __init__(self, name, ingredients_list, rating=None):
        super().__init__(name, ingredients_list, rating)

    @property
    def core_ingredients(self):
        return self.ingredients_list[:Recipe.NUM_CORE]

    @property
    def extra_ingredients(self):
        return self.ingredients_list[Recipe.NUM_CORE:]

    def __repr__(self):
        s = f'(generated) Recipe for {self.name}'
        for i in self.ingredients_list:
            s += '\t' + i.__repr__() + '\n'
        return s


class Ingredient:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def __repr__(self):
        return f'{self.name}, {self.amount} grams'


def recipe_tf_idf(recipe, compare_to):
    """
    Returns a score from 0-1 saying, on average, how much each ingredient is unique to this recipe relative to other recipes.
    Args:
        recipe (Recipe): the recipe object to score
        compare_to (list[Recipe]): the other recipes to compare against
    """
    tf_idf_list = []
    for ingredient in recipe.ingredients_list[-recipe.num_extras:]:
        tf = ingredient.amount / (len(recipe.ingredients_list) * 20)

        # idf = log(len(compare_to) / total occurrences (OR amount) in compare_to)
        total_occurrences = 0
        for other_recipe in compare_to:
            for other_ingredient in other_recipe.ingredients_list:
                if other_ingredient.name == ingredient.name:
                    total_occurrences += 1

        idf = log10(len(compare_to) / total_occurrences)
        tf_idf = tf * idf
        tf_idf_list.append(tf_idf)

    return sum(tf_idf_list) / len(tf_idf_list)


def cup_to_g(name, amount):
    storage = amount / .25
    if name == "flour":
        amount = storage * 32
    elif name == "butter":
        amount = storage * 57
    elif name == "white sugar" or name == "confectioners' sugar":
        amount = storage * 50
    elif name == "brown sugar" or name == "sugar":
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
    elif name == "shortening":
        amount = storage * 47
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
        rating = parse_store[0]
        for ingredient in parse_store[1:]:
            if ingredient.get("name") == "butter, softened" or ingredient.get("name") == "unsalted butter, chilled":
                ingredient.update({"name": "butter"})
            if ingredient.get("name") == "egg" or ingredient.get("name") == "eggs":
                ingredient.update({"name": "egg(s)"})
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
        if rating > -1:
            recipe_list.append(Recipe(key, ingredients_list, rating))
        else:
            recipe_list.append(Recipe(key, ingredients_list))
    return recipe_list


def core_fitness(gen_recipe, recipe_list):
    pass


def main():
    recipe_dict = get_recipe_dict()
    recipe_list = translate(recipe_dict)
    p = Population(recipe_list)

    num_core = 8
    num_extras = 5
    for i in range(1, 10):
        new = p.generate(num_core, num_extras)
        print(recipe_tf_idf(new, p.recipes_list))


main()
