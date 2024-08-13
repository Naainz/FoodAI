from flask import Flask, render_template, request, redirect, url_for, flash
import os
import requests
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

def find_recipes(ingredients):
    ingr_list = ingredients.split(',')
    total_ingr = len(ingr_list)
    found_recipes = {}
    
    for ingr in ingr_list:
        meals = get_recipes_by_ingr(ingr.strip())
        if meals:
            for meal in meals:
                if meal['strMeal'] in found_recipes:
                    found_recipes[meal['strMeal']] += 1
                else:
                    found_recipes[meal['strMeal']] = 1
    
    recipes_to_output = {meal: int((count / total_ingr) * 100) for meal, count in found_recipes.items() if int((count / total_ingr) * 100) >= 50}
    
    return recipes_to_output

def detect_ingredients(image_path):
    results = model(image_path)
    detected_ingr = set()
    for result in results:
        for label in result.boxes.cls:
            ingredient = result.names[int(label)]
            if ingredient.lower() in food_items:
                detected_ingr.add(ingredient)
    
    base_name = os.path.basename(image_path)
    name, _ = os.path.splitext(base_name)
    save_path = f"static/yolo/{name}.jpg"
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    result.save(save_path)
    
    return list(detected_ingr), save_path

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

if __name__ == '__main__':
    app.run(debug=True)
