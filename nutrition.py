import requests

# A AI GENERATED LIST OF NUTRITIONAL VALUES
nutritional_db = {
    "chicken": {"calories": 165, "protein": 31, "fat": 3.6, "carbs": 0},
    "rice": {"calories": 130, "protein": 2.7, "fat": 0.3, "carbs": 28},
    "butter": {"calories": 717, "protein": 0.85, "fat": 81, "carbs": 0.1},
    "egg": {"calories": 155, "protein": 13, "fat": 11, "carbs": 1.1},
    "flour": {"calories": 364, "protein": 10, "fat": 1, "carbs": 76},
    "milk": {"calories": 42, "protein": 3.4, "fat": 1, "carbs": 5},
    "sugar": {"calories": 387, "protein": 0, "fat": 0, "carbs": 100},
    "salt": {"calories": 0, "protein": 0, "fat": 0, "carbs": 0},
}

def get_recipe_details(recipe_name):
    url = "https://www.themealdb.com/api/json/v1/1/search.php"
    params = {'s': recipe_name}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['meals']:
            return data['meals'][0]
        else:
            return None
    else:
        return None

def calculate_nutrition(ingredients):
    total_nutrition = {"calories": 0, "protein": 0, "fat": 0, "carbs": 0}
    for ingredient in ingredients:
        name = ingredient.lower()
        if name in nutritional_db:
            for key in total_nutrition:
                total_nutrition[key] += nutritional_db[name][key]
    return total_nutrition

def save_nutrition_to_file(recipe_name, nutrition, ingredients):
    file_name = f"{recipe_name}_nutrition.txt"
    with open(file_name, "w") as file:
        file.write(f"Nutrition Breakdown for {recipe_name}\n")
        file.write("=====================================\n")
        file.write("Ingredients:\n")
        for ingredient in ingredients:
            file.write(f"- {ingredient}\n")
        file.write("\nNutritional Information (approximate per serving):\n")
        file.write(f"Calories: {nutrition['calories']} kcal\n")
        file.write(f"Protein: {nutrition['protein']} g\n")
        file.write(f"Fat: {nutrition['fat']} g\n")
        file.write(f"Carbohydrates: {nutrition['carbs']} g\n")
    print(f"Nutrition information saved to {file_name}")

def main():
    recipe_name = input("Enter the name of the recipe: ").strip()
    recipe_details = get_recipe_details(recipe_name)
    
    if recipe_details:
        ingredients = [recipe_details[f'strIngredient{i}'] for i in range(1, 21) if recipe_details[f'strIngredient{i}']]
        nutrition = calculate_nutrition(ingredients)
        save_nutrition_to_file(recipe_name, nutrition, ingredients)
    else:
        print(f"Recipe for '{recipe_name}' not found.")

if __name__ == "__main__":
    main()
