"""
Authors: Danny Little, Bruce Tang, August Wadlington
CSCI 3725
Last Edited: 2021-03-30
"""

import random
from math import log10
from os import *
from os.path import isfile
from clean_text import get_recipe_dict
import unit_conversion as u_convert
import numpy as np
from itertools import combinations

WORD_EMBED_VALS = np.load('ingred_word_emb.npy', allow_pickle=True).item()


def ingredient_similarity(n1, n2):
    """
    Takes in two ingredients, and compares them using vectors generated from the
    ingred_word_emb.npy file
    Args:
        n1 (String): a string representing an ingredient name
        n2 (String): a string representing an ingredient name
    """
    if " " not in n1 and " " not in n2:
        return ingredient_vector(n1, n2)

    biggest = -1
    if " " not in n1:
        for word in n2.split(" "):
            vec = ingredient_vector(n1, word)
            if vec:
                biggest = max(biggest, vec)

    elif " " not in n2:
        for word in n1.split(" "):
            vec = ingredient_vector(word, n2)
            if vec:
                biggest = max(biggest, vec)

    else:
        n1_words = n1.split(" ")
        n2_words = n2.split(" ")
        for n1 in n1_words:
            for n2 in n2_words:
                vec = ingredient_vector(n1, n2)
                if vec:
                    biggest = max(biggest, vec)

    if biggest == -1:
        return None
    return biggest


def ingredient_vector(n1, n2):
    """
    Returns the overlap of two ingredients after vectorizing them based on the flavor pairing
    database included with the program.
    Args:
        n1 (String): a string representing the name of an ingredient
        n2 (String): a string representing the name of an ingredient
    """
    v1 = WORD_EMBED_VALS.get(n1, [])
    v2 = WORD_EMBED_VALS.get(n2, [])

    if len(v1) > 0 and len(v2) > 0:
        return np.dot(v1, v2)
    return None


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
        """
        Store each ingredient name and its frequency in a dictionary. 
        """
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
        recipe_name = random.choice(extra)
        while i > 0:
            extra_ingredient_name = random.choice(extra)
            extra.remove(extra_ingredient_name)
            extra_objects = self.all_ingredient_objects.get(
                extra_ingredient_name)
            extra_amount = random.choice(extra_objects)
            output_ingredient_list.append(
                Ingredient(extra_ingredient_name, extra_amount.amount))
            i -= 1

        recipe_name += " cookie"

        return GeneratedRecipe(recipe_name, output_ingredient_list)

    def fitness(self, recipe, compare_to=None):
        """
        Returns a score from 0-1 saying, on average, how fit this cookie is against our chosen metrics (novelty and value)
        Args:
            compare_to (list[Recipe]): the other recipes to compare against
        """
        evaluations = [self.recipe_tf_idf(
            recipe, compare_to), self.core_fitness(recipe)]
        similarity = recipe.extras_similarity()
        if similarity:
            evaluations.append(similarity)

        return sum(evaluations) / len(evaluations)

    def recipe_tf_idf(self, recipe, compare_to=None):
        """
        Returns a score from 0-1 saying, on average, how much each ingredient is unique to this recipe relative to other recipes.
        Args:
            compare_to (list[Recipe]): the other recipes to compare against
        """
        if not compare_to:
            compare_to = self.recipes_list
        tf_idf_list = []
        # for ingredient in recipe.ingredients_list[-recipe.num_extras:]:
        for ingredient in recipe.extra_ingredients:
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

    def core_fitness(self, recipe):
        """
        Returns a score from 0-1 of how close the amount of core ingredient selected is to the amount these
        same ingredients are used in the original recipes
        Args:
            recipe_gen (Recipe): the recipe the system generated
            recipe_dict ([string: list(recipe)]): the recipes parsed to compare with
        """
        score = 0
        for ingredient in recipe.core_ingredients:
            ingredient_name = ingredient.name
            ingredient_object_list = self.all_ingredient_objects.get(
                ingredient_name)
            sum = 0
            for object in ingredient_object_list:
                sum += object.amount
            average_amount = sum / len(ingredient_object_list)
            fitness = (average_amount - ingredient.amount) / average_amount
            if fitness < 0:
                fitness *= -1
            score += fitness

        return score / Recipe.NUM_CORE


class Recipe:
    NUM_CORE = 10

    def __init__(self, name, ingredients_list, rating=None):
        """
        This class represents a recipe object, containing a list of ingredients, name,
        and potential rating based on whether it had a rating on the website it
        was pulled from
        Args:
            name (String): a string representing the given name of the recipe
            ingredients_list (list<Ingredient>): a list containing recipe's ingredients and their respective amounts
        """
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
        """
        This method finds the percentage off from 100 oz the recipe's sum of ingredients is,
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

    def extras_similarity(self):
        """
        Checks the extra ingredients in the parent recipe to test for how similar they are in the
        flavor parings database ingred_word_emb.npy
        """
        similarities = []
        for ing1, ing2 in list(combinations(self.extra_ingredients, 2)):
            sim = ingredient_similarity(ing1.name, ing2.name)
            if sim:
                similarities.append(sim)
        if similarities:
            return sum(similarities) / len(similarities)
        return None

    def __repr__(self):
        s = f'(generated) Recipe for {self.name}:\n'
        for i in self.ingredients_list:
            s += '\t' + i.__repr__() + '\n'
        return s + '\n'


def translate(recipe_dict):
    """
    This method will correct for some naming conventions in various recipes,
    as well as standardizing ingredients names for parsing and generation.
    This assumes that all butter is softened and doesn't make note of salted
    vs not (if relevant, may need to experiment)
    """
    recipe_list = []
    for key in list(recipe_dict.keys()):
        parse_store = recipe_dict.get(key)
        ingredients_list = []
        rating = parse_store[0]
        for ingredient in parse_store[1:]:
            """Not all butter is equal, but the generator treats it as if it were"""
            if ingredient.get("name") == "butter, softened" or ingredient.get("name") == "unsalted butter, chilled":
                ingredient.update({"name": "butter"})
            if ingredient.get("name") == "egg" or ingredient.get("name") == "eggs":
                ingredient.update({"name": "egg(s)"})
            if ingredient.get("unit") == "teaspoons" or ingredient.get("unit") == "teaspoon":
                cup_from_tspoon = u_convert.tspoon_to_cup(ingredient.get("amount"))
                ingredient.update({"amount": cup_from_tspoon})
                ingredient.update({"unit": "cups"})
            if ingredient.get("unit") == "tablespoon" or ingredient.get("unit") == "tablespoons":
                cup_from_tbspoon = u_convert.tbspoon_to_cup(ingredient.get("amount"))
                ingredient.update({"amount": cup_from_tbspoon})
                ingredient.update({"unit": "cups"})
            if ingredient.get("unit") == "cup" or ingredient.get("unit") == "cups":
                grams_from_cups = u_convert.cup_to_g(ingredient.get(
                    "name"), ingredient.get("amount"))
                ingredient.update({"amount": grams_from_cups})
                ingredient.update({"unit": "grams"})
            if ingredient.get("unit") == "ounce" or ingredient.get("unit") == "oz" or ingredient.get("unit") == "ounces":
                g_from_oz = u_convert.oz_to_g(ingredient.get("amount"))
                ingredient.update({"amount": g_from_oz})
                ingredient.update({"unit": "grams"})

            ingredients_list.append(Ingredient(
                ingredient.get("name"), ingredient.get("amount")))
        if rating > -1:
            recipe_list.append(Recipe(key, ingredients_list, rating))
        else:
            recipe_list.append(Recipe(key, ingredients_list))
    return recipe_list


class Ingredient:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def __repr__(self):
        return f'{self.name}, {self.amount} grams'


def main():
    recipe_dict = get_recipe_dict()
    recipe_list = translate(recipe_dict)
    p = Population(recipe_list)

    new = p.generate(Recipe.NUM_CORE, 5)

    # # Get top 5 out of 100 generated
    generated = []
    for i in range(100):
        num_extras = random.randint(4, 6)
        new = p.generate(Recipe.NUM_CORE, num_extras)
        fitness = p.fitness(new)
        generated.append((new, fitness))

    generated.sort(key=lambda x: x[1], reverse=True)
    top_five = generated[:5][::-1]
    for recipe, fitness in top_five:
        print(fitness)
        print(recipe)


main()
