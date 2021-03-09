import requests
from bs4 import BeautifulSoup


def get_cookie_type_urls():
    cookie_categories_url = "https://www.allrecipes.com/recipes/362/desserts/cookies/"
    html = requests.get(cookie_categories_url).text
    soup = BeautifulSoup(html, 'lxml')
    recipes_raw = soup.find_all(
        'a', class_='carouselNav__link recipeCarousel__link')

    recipes = []
    for recipe_raw in recipes_raw:
        recipe_href = recipe_raw.get('href')
        split_url = [href for href in recipe_href.split('/') if href]
        if "cookie" in split_url[-1] and split_url[-2] != "frostings-and-icings":
            recipes.append(recipe_href)
    return recipes


def get_recipe_urls(cookie_type_url, number):
    recipe_urls = []
    html = requests.get(cookie_type_url).text
    soup = BeautifulSoup(html, 'lxml')
    recipe_cards = soup.find_all('div', class_='card__detailsContainer')

    for i in range(number):
        card = recipe_cards[i]
        recipe_urls.append(card.a.get('href'))
    return recipe_urls


def make_recipe_file(url):
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

    for ingredient in ingredients_raw:
        recipe_file_text += ingredient.text.strip() + '\n'

    with open('recipes/' + recipe_name + '.txt', 'w') as file:
        file.truncate(0)
        file.write(recipe_file_text)


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