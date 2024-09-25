from bs4 import BeautifulSoup
import requests
import re

main_url = "https://kulinaria.ge"
my_category = "თევზი და ზღვის პროდუქტები"
recipe_list = []

url = requests.get(main_url)
main_soup = BeautifulSoup(url.text, "html.parser")

recipes_url = main_url + main_soup.find('a', class_="nav__item recipe-nav-text").attrs['href']
recipes_soup = BeautifulSoup(requests.get(recipes_url).text, "html.parser")

category_url = main_url + recipes_soup.find("div", string=my_category).find_parent("a").attrs['href']
category_soup = BeautifulSoup(requests.get(category_url).text, "html.parser")

subcategories = category_soup.find("div", class_="recipe__nav--view").find_all("a", class_="recipe__nav-item")

for subcategory in subcategories:
    subcategory_title = subcategory.find("div", class_="txt").text
    subcategory_url = main_url + subcategory.attrs['href']
    subcategory_soup = BeautifulSoup(requests.get(subcategory_url).text, "html.parser")

    recipes = subcategory_soup.find_all("div", class_="box box--author kulinaria-col-3 box--massonry")

    for recipe in recipes:
        title = recipe.find('a', class_="box__title").text.strip()
        author = recipe.find('div', class_="name").text.strip()
        desc = recipe.find('div', class_="box__desc").text.strip()
        image_url = main_url + recipe.find('img').attrs['src']
        recipe_url = main_url + recipe.find('a', class_="box__title").attrs['href']
        request_url = requests.get(recipe_url)
        recipe_soup = BeautifulSoup(request_url.text, "html.parser")
        portion_text = recipe_soup.find('div', class_="kulinaria-sprite kulinaria-sprite--circleprogress").find_parent('div').text.strip()
        match = re.search(r'\d+', portion_text)
        portion = int(match.group()) if match else 0
        recipe_ingredients = recipe_soup.find_all("div", class_="list__item")
        recipe_cooking_steps = recipe_soup.find_all("div", class_="lineList__item")

        cooking_steps = []
        for step in recipe_cooking_steps:
            cooking_steps.append(f"{step.div.text}. {step.p.text.strip()}")

        # Create recipe ingredients list
        ingredients = []
        for ingredient in recipe_ingredients:
            raw_text = ingredient.get_text(separator=' ', strip=True)
            clean_text = ' '.join(raw_text.split())
            ingredients.append(clean_text)


        recipe_list.append(
            {"Title": title,
             "Recipe URL": recipe_url,
             "Main Category": {"Title": my_category, "url": category_url},
             "Subcategory": {"Title": subcategory_title, "url": subcategory_url},
             "Image URL": image_url,
             "Description": desc,
             "Author": author,
             "Portion": portion,
             "Ingredients": ingredients,
             "Cooking Steps": cooking_steps
             }
        )