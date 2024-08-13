from flask import Flask, render_template, request
import requests

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
