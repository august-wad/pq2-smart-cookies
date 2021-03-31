"""
Authors: Danny Little, Bruce Tang, August Wadlington
CSCI 3725
Last Edited: 2021-03-30

This file will scrape cookie recipes from allrecipes.com, do some initial
parsing, and then store each recipe in its own text file. The functions
ues the BeautifulSoup package to parse the HTML. This file should NOT be run,
unless you want to re-scrape all of the text file, which may take ~5 minutes or so!

Prof. Harmon suggested that recipes could be stored instead in a .npy file,
but  doing so ended up being tricky because each recipe may have a
different number of ingredients. 
"""


import requests
from bs4 import BeautifulSoup


def get_cookie_type_urls():
    """
    Finds the URL's for categories of cookies listed at the following URL:
    https://www.allrecipes.com/recipes/362/desserts/cookies/
    """
    cookie_categories_url = "https://www.allrecipes.com/recipes/362/desserts/cookies/"
    html = requests.get(cookie_categories_url).text
    soup = BeautifulSoup(html, 'lxml')
    types_raw = soup.find_all(
        'a', class_='carouselNav__link recipeCarousel__link')

    type_urls = []
    for type_raw in types_raw:
        type_href = type_raw.get('href')
        split_url = [href for href in type_href.split('/') if href]
        if "cookie" in split_url[-1] and split_url[-2] != "frostings-and-icings":
            type_urls.append(type_href)
    return type_urls


def get_recipe_urls(cookie_type_url, number):
    """
    Returns a specified number of recipe URL's from a given page that contains
    a list of cookie recipes of one kind of cookie.
        Args:
        cookie_type_url (str): the URL of this cookie type.
        number (int): the number of recipe URL's to return.
    """
    recipe_urls = []
    html = requests.get(cookie_type_url).text
    soup = BeautifulSoup(html, 'lxml')
    recipe_cards = soup.find_all('div', class_='card__detailsContainer')

    for i in range(number):
        card = recipe_cards[i]
        recipe_urls.append(card.a.get('href'))
    return recipe_urls


def make_recipe_file(url):
    """
    Makes and writes to a file the name of a recipe, along with its ingredients
    and the amount of each ingredient, with some processing involved.
    """
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'lxml')
    recipe_name = soup.head.title.text
    if recipe_name.endswith("Recipe | Allrecipes"):
        recipe_name = recipe_name[:-20]
    elif recipe_name.endswith(" | Allrecipes"):
        recipe_name = recipe_name[:-14]

    ingredients_raw = soup.find_all('li', class_='ingredients-item')
    if not ingredients_raw:
        return

    recipe_file_text = recipe_name + '\n'
    recipe_rating = soup.find('span', class_='review-star-text')
    recipe_file_text += recipe_rating.text.strip() + '\n'

    for ingredient in ingredients_raw:
        recipe_file_text += clean_ingredient_text(ingredient.text)

    with open('recipes/' + recipe_name + '.txt', 'w') as file:
        file.truncate(0)
        file.write(recipe_file_text)


def clean_ingredient_text(ingredient_str):
    """
    cleans up the text of a recipe's ingredients to make it easier to work with.
    Primarily calls a helper function to replace single unicode character
    with appropriate decimal values. 
    """
    ugly_fractions = {'¼', '½', '¾', '⅐', '⅑', '⅒', '⅓', '⅔',
                      '⅕', '⅖', '⅗', '⅘', '⅙', '⅚', '⅛', '⅜', '⅝', '⅞'}

    ing_stripped = ingredient_str.strip()
    cleaned = ing_stripped.replace('\u2009', '') + '\n'
    if cleaned[1] in ugly_fractions:
        mixed_fraction = float(cleaned[0]) + get_annoying_fraction(cleaned[1])
        cleaned = str(mixed_fraction) + cleaned[2:]
    elif cleaned[0] in ugly_fractions:
        cleaned = str(get_annoying_fraction(cleaned[0])) + cleaned[1:]
    return cleaned


def get_annoying_fraction(fraction):
    """
    A function for converting single unicode fraction characters into their float values. 
    """
    return {'¼': 1/4, '½': .5, '¾': 3/4, '⅐': 1/7, '⅑': 1/9, '⅒': .1, '⅓': 1/3, '⅔': 2/3, '⅕': .2, '⅖': .4, '⅗': .6, '⅘': .8, '⅙': 1/6, '⅚': 5/6, '⅛': 1/8, '⅜': 3/8, '⅝': 5/8, '⅞': 7/8}.get(fraction)


def main():

    # get urls for allrecipe's ~24 categories
    cookie_type_urls = get_cookie_type_urls()
    # above urls link to ~12 actual recipes. For now, grab the first 5 and make files from contents.
    recipe_urls = []
    for url in cookie_type_urls:
        recipe_urls += get_recipe_urls(url, 8)

    for recipe_url in list(set(recipe_urls)):
        make_recipe_file(recipe_url)


main()
