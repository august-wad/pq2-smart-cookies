
class Ingredient:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount


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



def cup_to_g(name, amount):
    """
    Takes in an ingredient with measurement unit cups and converts
    it to the proper amount in grams
    """
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
    """
    Converts a teaspoon amount to cups
    """
    return amount * .0208



def tbspoon_to_cup(amount):
    """
    Converts a tablespoon amount to cups
    """
    return amount * .0625