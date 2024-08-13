import requests

def get_recipes_by_ingr(ingr):
    url = "https://www.themealdb.com/api/json/v1/1/filter.php"
    params = {'i': ingr}
    res = requests.get(url, params=params)
    if res.status_code == 200:
        data = res.json()
        if 'meals' in data:
            return data['meals']
        else:
            return None
    else:
        return None

def main():
    ingr_list = input("Enter the ingredients you have (comma-separated): ").split(',')
    total_ingr = len(ingr_list)
    found_recipes = {}
    output_count = 0
    
    for ingr in ingr_list:
        meals = get_recipes_by_ingr(ingr.strip())
        if meals:
            for meal in meals:
                if meal['strMeal'] in found_recipes:
                    found_recipes[meal['strMeal']] += 1
                else:
                    found_recipes[meal['strMeal']] = 1
    
    if found_recipes:
        with open("found_recipes.txt", "w") as file:
            file.write("Available Ingredients: " + ', '.join(ingr_list) + "\n\n")
            
            # Calculate how many recipes have >= 50% of the ingredients
            recipes_to_output = {meal: int((count / total_ingr) * 100) for meal, count in found_recipes.items() if int((count / total_ingr) * 100) >= 50}
            output_count = len(recipes_to_output)
            
            file.write(f"Found Recipes ({output_count}):\n")
            for meal, percentage in recipes_to_output.items():
                file.write(f"- {meal} [{percentage}%]\n")
        
        print(f"Recipes have been saved to 'found_recipes.txt' (Total: {output_count})")
    else:
        print("No recipes found with the given ingredients.")

if __name__ == "__main__":
    main()
