from flask import Flask, render_template, request, redirect, url_for, flash
import os
import requests
import random
from datetime import datetime
from ultralytics import YOLO
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads/'


os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

model = YOLO('yolov8x.pt')

common_allergens = {
    "milk", "eggs", "fish", "shellfish", "tree nuts", "peanuts", 
    "wheat", "soybeans", "gluten", "sesame"
}

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

def calculate_bmr(age, height, weight, gender):
    if gender.lower() == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender.lower() == 'female':
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        raise ValueError("Gender must be 'male' or 'female'")
    return bmr

def activity_multiplier(level):
    if level == 1:
        return 1.2
    elif level == 2:
        return 1.375
    elif level == 3:
        return 1.55
    elif level == 4:
        return 1.725
    elif level == 5:
        return 1.9
    else:
        raise ValueError("Activity level must be between 1 and 5")

def calculate_daily_calories(bmr, goal, activity_level):
    tdee = bmr * activity_multiplier(activity_level)
    if goal.lower() == 'gain':
        return tdee + 500
    elif goal.lower() == 'lose':
        return tdee - 500
    elif goal.lower() == 'maintain':
        return tdee
    else:
        raise ValueError("Goal must be 'gain', 'lose', or 'maintain'")

def get_meal_details(meal_name):
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={meal_name}"
    response = requests.get(url)
    if response.status_code == 200:
        meals = response.json().get('meals')
        if meals:
            return meals[0]
        else:
            print(f"No details found for meal: {meal_name}")
            return None
    else:
        print(f"Failed to fetch details for meal name: {meal_name}. HTTP Status Code: {response.status_code}")
        return None

def simulate_calories(meal_details):
    num_ingredients = sum(1 for i in range(1, 21) if meal_details[f'strIngredient{i}'])
    return random.randint(200, 500) + (num_ingredients * 10)

def attempt_get_meal(category, retries=5, fallback_to_random=True):
    predefined_meals = [
        "Arrabiata", "Bolognese", "Taco", "Paella", "Ratatouille", "Beef Wellington", 
        "Caesar Salad", "Chicken Alfredo", "Fish and Chips", "Lamb Chops", "Moussaka", 
        "Pancakes", "Pizza", "Ramen", "Spaghetti Carbonara", "Vegetable Stir Fry", 
        "Butter Chicken", "Ceviche", "Dumplings", "Fried Rice", "Goulash", "Jambalaya",
        "Kebab", "Lasagna", "Meatballs", "Nachos", "Omelette", "Pad Thai", 
        "Quesadilla", "Risotto", "Shepherd's Pie", "Sushi", "Tiramisu", "Udon", 
        "Vindaloo", "Waffles", "Xiaolongbao", "Yakitori", "Zucchini Bread"
    ]

    for attempt in range(retries):
        meal_name = random.choice(predefined_meals)
        meal_details = get_meal_details(meal_name)
        if meal_details:
            return meal_details
        else:
            predefined_meals.remove(meal_name)  
            if not predefined_meals:
                break  
        print(f"Attempt {attempt + 1} for {category or 'Any'} failed.")
    
    if fallback_to_random:
        print("Fallback failed for all predefined meals.")
        return None
    
    print(f"Failed to retrieve a meal for category: {category or 'Any'} after {retries} attempts.")
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main', methods=['GET', 'POST'])
def generate_meals():
    if request.method == 'POST':
        ingredients = request.form.get('ingredients')
        recipes = find_recipes(ingredients)
        return render_template('main.html', recipes=recipes, ingredients=ingredients)
    return render_template('main.html')

@app.route('/yolo', methods=['GET', 'POST'])
def yolo():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            detected_ingr, save_path = detect_ingredients(filepath)
            recipes = find_recipes(','.join(detected_ingr))
            return render_template('yolo.html', ingredients=detected_ingr, recipes=recipes, image_url=save_path)
    return render_template('yolo.html')

@app.route('/allergy', methods=['GET', 'POST'])
def allergy():
    if request.method == 'POST':
        recipe_name = request.form.get('recipe_name')
        recipe_details = get_recipe_details(recipe_name)
        if recipe_details:
            ingredients = [recipe_details[f'strIngredient{i}'] for i in range(1, 21) if recipe_details[f'strIngredient{i}']]
            allergens = check_allergens(ingredients)
            return render_template('allergy.html', recipe_name=recipe_name, allergens=allergens)
        else:
            flash(f"No recipe found for '{recipe_name}'")
            return redirect(request.url)
    return render_template('allergy.html')

@app.route('/nutrition', methods=['GET', 'POST'])
def nutrition():
    if request.method == 'POST':
        recipe_name = request.form.get('recipe_name')
        recipe_details = get_recipe_details(recipe_name)
        if recipe_details:
            ingredients = [recipe_details[f'strIngredient{i}'] for i in range(1, 21) if recipe_details[f'strIngredient{i}']]
            nutrition = calculate_nutrition(ingredients)
            return render_template('nutrition.html', recipe_name=recipe_name, nutrition=nutrition, ingredients=ingredients)
        else:
            flash(f"No recipe found for '{recipe_name}'")
            return redirect(request.url)
    return render_template('nutrition.html')

@app.route('/plan', methods=['GET', 'POST'])
def plan():
    if request.method == 'POST':
        age = int(request.form.get('age'))
        height = float(request.form.get('height'))
        weight = float(request.form.get('weight'))
        gender = request.form.get('gender')
        goal = request.form.get('goal').strip().lower()
        activity_level = int(request.form.get('activity_level'))

        bmr = calculate_bmr(age, height, weight, gender)
        daily_calories = calculate_daily_calories(bmr, goal, activity_level)
        target_calories = daily_calories * 0.9  

        meal_plan = {
            "breakfast": "Breakfast",
            "lunch": "Lunch",
            "dinner": "Dinner",
            "snack": "Dessert"  
        }

        total_calories = 0
        meal_details_list = []

        for meal, category in meal_plan.items():
            meal_details = attempt_get_meal(category)
            if meal_details:
                calories = simulate_calories(meal_details)
                total_calories += calories
                meal_details_list.append((meal, meal_details['strMeal'], calories))
            else:
                print(f"Skipping {meal} due to lack of data.")

        if total_calories > target_calories:
            excess_calories = total_calories - target_calories
            while excess_calories > 0 and meal_details_list:
                meal, details, calories = meal_details_list.pop()
                excess_calories -= calories
                total_calories -= calories

        return render_template('plan.html', meal_details_list=meal_details_list, total_calories=total_calories, target_calories=target_calories)

    return render_template('plan.html')

if __name__ == '__main__':
    app.run(debug=True)
