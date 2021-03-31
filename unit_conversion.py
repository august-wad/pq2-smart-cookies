def oz_to_g(amount):
    return (amount * 28)

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