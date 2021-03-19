"""
Authors: Danny Little, Bruce Tang, August Wadlington
CSCI 3725
Last Edited: 2021-03-18
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
        """Generate a recipe from picking certain number of core and extra ingredients by number of 
        frequencies they have shown up in aspiring recipes. 
            Args:
                num_core: number of core ingredients to choose from; it's set to 10 by default,
                when num_core is greater ten, the function generate ten out of num_core by probabilities,
                and when num_core is less than ten the function selects num_core core ingredients
                num_extras: number of extra ingredients desired. Selected from the ingreidents left
                after core ingredients have been selected.
        """
        freqency_map = self.freq_ingredients()
        output_ingredient_list = []
        self.all_ingredients.sort(
            key=lambda ingredient: freqency_map.get(ingredient), reverse=True)
        core = self.all_ingredients[:num_core]

        # select 10 core ingredients probabilistically from top num_core ingredients
        # unless num_core is less than 10, in which case just pick the top core_num ingredients
        ingre_freq = [freqency_map.get(ingre)
                      for ingre in self.all_ingredients][:num_core]
        while len(output_ingredient_list) < Recipe.NUM_CORE:
            if (len(output_ingredient_list) == num_core):
                break
            ingredient = random.choices(core, weights=ingre_freq)[0]
            core.remove(ingredient)
            ingre_freq = [freqency_map.get(ingre)
                          for ingre in core]

            ingredient_objects = self.all_ingredient_objects.get(ingredient)
            high = max(
                i.amount for i in ingredient_objects)
            low = min(
                i.amount for i in ingredient_objects)
            new_amount = random.uniform(low, high)
            output_ingredient_list.append(
                Ingredient(ingredient, new_amount))

        # and the rest is the extra pool
        extra = list(set(self.all_ingredients) - set(core))
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
        return s + '\n'


class GeneratedRecipe(Recipe):
    def __init__(self, name, ingredients_list, rating=None):
        super().__init__(name, ingredients_list, rating)

    @property
    def core_ingredients(self):
        return self.ingredients_list[:Recipe.NUM_CORE]

    @property
    def extra_ingredients(self):
        return self.ingredients_list[Recipe.NUM_CORE:]

    def core_fitness(self, recipe_dict):
        """
        Returns a score from 0-1 of how close the amount of core ingredient selected is to the amount these
        same ingredients are used in the original recipes
        Args:
            recipe_gen (Recipe): the recipe the system generated
            recipe_dict ([string: list(recipe)]): the recipes parsed to compare with
        """
        score = 0
        for ingredient in self.core_ingredients:
            ingredient_name = ingredient.name
            ingredient_object_list = recipe_dict.get(ingredient_name)
            sum = 0
            for object in ingredient_object_list:
                sum += object.amount
            average_amount = sum / len(ingredient_object_list)
            fitness = (average_amount - ingredient.amount) / average_amount
            if fitness < 0:
                fitness *= -1
            score += fitness

        return score / Recipe.NUM_CORE

    def recipe_tf_idf(self, compare_to):
        """
        Returns a score from 0-1 saying, on average, how much each ingredient is unique to this recipe relative to other recipes.
        Args:
            compare_to (list[Recipe]): the other recipes to compare against
        """
        tf_idf_list = []
        # for ingredient in recipe.ingredients_list[-recipe.num_extras:]:
        for ingredient in self.extra_ingredients:
            tf = ingredient.amount / (len(self.ingredients_list) * 20)

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

    def __repr__(self):
        s = f'(generated) Recipe for {self.name}:\n'
        for i in self.ingredients_list:
            s += '\t' + i.__repr__() + '\n'
        return s + '\n'

    def fitness(self, compare_to, recipe_dict):
        return (self.recipe_tf_idf(compare_to) + self.core_fitness(recipe_dict)) / 2


class Ingredient:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def __repr__(self):
        return f'{self.name}, {self.amount} grams'


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


def main():
    recipe_dict = get_recipe_dict()
    recipe_list = translate(recipe_dict)
    p = Population(recipe_list)
    for i in range(3):
        new = p.generate(Recipe.NUM_CORE, 5)
        print("Core:")
        print(new.core_ingredients)
        print("Extra:")
        print(new.extra_ingredients)
        print("Fitness:" + str(new.fitness(p.recipes_list, p.all_ingredient_objects)))

    # # Get top 5 out of 100 generated
    # generated = []
    # for i in range(100):
    #     num_extras = random.randint(4, 6)
    #     new = p.generate(Recipe.NUM_CORE, num_extras)
    #     fitness = core_fitness(new, p.all_ingredient_objects) + \
    #         recipe_tf_idf(new, p.recipes_list) / 2
    #     generated.append((new, fitness))

    # generated.sort(key=lambda x: x[1], reverse=True)
    # print(generated[:5])


main()
