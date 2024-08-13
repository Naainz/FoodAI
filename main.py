import requests

def get_recipes_by_ingr(ingr):
    
    url = "https://www.themealdb.com/api/json/v1/1/filter.php"
    
    
    params = {
        'i': ingr
    }
    
    
    res = requests.get(url, params=params)
    
    
    if res.status_code == 200:
        data = res.json()
        if 'meals' in data:
            return data['meals']
        else:
            return None
    else:
        print("Error:", res.status_code)
        return None

def main():
    
    ingr_list = input("Enter the ingredients you have (comma-separated): ").split(',')
    
    
    found_recipes = set()
    
    
    for ingr in ingr_list:
        meals = get_recipes_by_ingr(ingr.strip())
        if meals:
            for meal in meals:
                found_recipes.add(meal['strMeal'])
    
    
    if found_recipes:
        print("Found recipes:")
        for meal in found_recipes:
            print(f"- {meal}")
    else:
        print("No recipes found with the given ingredients.")

if __name__ == "__main__":
    main()
