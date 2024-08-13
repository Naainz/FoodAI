import requests

common_allergens = {
    "milk", "eggs", "fish", "shellfish", "tree nuts", "peanuts", 
    "wheat", "soybeans", "gluten", "sesame"
}

def get_recipe_details(recipe_name):
    url = "https://www.themealdb.com/api/json/v1/1/search.php"
    params = {'s': recipe_name}
    res = requests.get(url, params=params)
    if res.status_code == 200:
        data = res.json()
        if 'meals' in data and data['meals']:
            return data['meals'][0]
        else:
            return None
    else:
        return None

def check_allergens(ingredients):
    found_allergens = set()
    for ingredient in ingredients:
        for allergen in common_allergens:
            if allergen.lower() in ingredient.lower():
                found_allergens.add(allergen)
    return found_allergens

def main():
    try:
        with open("found_recipes.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("found_recipes.txt not found. Make sure the file exists.")
        return
    
    recipe_names = [line.split('[')[0].strip('- ').strip() for line in lines if '-' in line]
    
    with open("allergies.txt", "w") as outfile:
        for recipe_name in recipe_names:
            recipe_details = get_recipe_details(recipe_name)
            if recipe_details:
                ingredients = [recipe_details[f'strIngredient{i}'] for i in range(1, 21) if recipe_details[f'strIngredient{i}']]
                allergens = check_allergens(ingredients)
                if allergens:
                    outfile.write(f"Recipe: {recipe_name}\n")
                    outfile.write(f"Allergens: {', '.join(allergens)}\n\n")
        print("Allergens have been checked and saved to 'allergies.txt'")

if __name__ == "__main__":
    main()
