import requests
from ultralytics import YOLO

model = YOLO('yolov8x.pt')


food_items = {
    "banana", "apple", "orange", "carrot", "broccoli", "cake", "sandwich", 
    "hot dog", "pizza", "donut", "banana", "carrot", "broccoli", "spoon", 
    "fork", "knife", "bottle", "cup", "wine glass", "bowl", "spoon", 
    "bread", "cake", "cookie", "cucumber", "egg", "garlic", "grape", 
    "lemon", "lime", "onion", "pear", "pepper", "plum", "potato", 
    "pumpkin", "strawberry", "tomato", "watermelon", "pineapple", 
    "kiwi", "mango", "pear", "peach", "avocado", "cabbage", "lettuce",
    "meat", "fish", "chicken", "beef", "pork", "bacon", "sausage",
    "rice", "pasta", "noodles", "cheese", "butter", "yogurt", "milk",
    "cream", "chocolate", "coffee", "tea", "sugar", "salt", "pepper",
    "spices", "honey", "jam", "syrup", "flour", "oil", "vinegar"
}

def detect_ingredients(image_path):
    results = model(image_path)
    detected_ingr = set()
    for result in results:
        for label in result.boxes.cls:
            ingredient = result.names[int(label)]
            if ingredient.lower() in food_items:
                detected_ingr.add(ingredient)
    return list(detected_ingr)

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

def main(image_path):
    detected_ingr = detect_ingredients(image_path)
    total_ingr = len(detected_ingr)
    found_recipes = {}
    output_count = 0
    
    for ingr in detected_ingr:
        meals = get_recipes_by_ingr(ingr)
        if meals:
            for meal in meals:
                if meal['strMeal'] in found_recipes:
                    found_recipes[meal['strMeal']] += 1
                else:
                    found_recipes[meal['strMeal']] = 1
    
    if found_recipes:
        with open("found_recipes.txt", "w") as file:
            file.write("Available Ingredients [FOUND BY AI]: " + ', '.join(detected_ingr) + "\n\n")
            recipes_to_output = {meal: int((count / total_ingr) * 100) for meal, count in found_recipes.items() if int((count / total_ingr) * 100) >= 50}
            output_count = len(recipes_to_output)
            file.write(f"Found Recipes ({output_count}):\n")
            for meal, percentage in recipes_to_output.items():
                file.write(f"- {meal} [{percentage}%]\n")
        print(f"Recipes with found ingredients have been saved to 'found_recipes.txt' (Total: {output_count})")
    else:
        with open("found_recipes.txt", "w") as file:
            file.write("Available Ingredients [FOUND BY AI]: " + ', '.join(detected_ingr) + "\n\n")
            file.write("Found Recipes (0):\n")
            file.write("- \n")
        print("No recipes found with the given ingredients.")

if __name__ == "__main__":
    image_path = input("Enter the path to the image file: ")
    main(image_path)
