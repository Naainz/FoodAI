import requests

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

def save_recipe_to_file(recipe_name, recipe_details):
    file_name = f"{recipe_name}.txt"
    with open(file_name, "w") as file:
        file.write(f"Recipe for {recipe_name}\n")
        file.write("Ingredients:\n")
        for i in range(1, 21):
            ingredient = recipe_details[f'strIngredient{i}']
            measure = recipe_details[f'strMeasure{i}']
            if ingredient and ingredient.strip():
                file.write(f"- {ingredient} ({measure.strip()})\n")
        file.write("\nRecipe:\n")
        file.write(recipe_details['strInstructions'])
    
    print(f"Recipe saved to {file_name}")

def main():
    recipe_name = input("Enter the name of the recipe: ").strip()
    recipe_details = get_recipe_details(recipe_name)
    
    if recipe_details:
        save_recipe_to_file(recipe_name, recipe_details)
    else:
        print(f"Recipe for '{recipe_name}' not found.")

if __name__ == "__main__":
    main()
