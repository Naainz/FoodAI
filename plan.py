import os
import requests
import random
from datetime import datetime

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

def save_meal_to_file(meal_details, file_name):
    with open(file_name, "w") as file:
        file.write(f"{meal_details['strMeal']}\n\n")
        file.write("Ingredients:\n")
        for i in range(1, 21):
            ingredient = meal_details[f'strIngredient{i}']
            measure = meal_details[f'strMeasure{i}']
            if ingredient and ingredient.strip():
                file.write(f"- {ingredient} ({measure.strip()})\n")
        file.write("\nInstructions:\n")
        file.write(meal_details['strInstructions'])

def attempt_get_meal(category, retries=3, fallback_to_random=True):
    predefined_meals = ["Arrabiata", "Bolognese", "Taco", "Paella", "Ratatouille"]

    for attempt in range(retries):
        if category:
            meal_name = random.choice(predefined_meals)
            meal_details = get_meal_details(meal_name)
            if meal_details:
                return meal_details
        print(f"Attempt {attempt + 1} for {category or 'Any'} failed.")
    
    if fallback_to_random:
        random_meal_name = random.choice(predefined_meals)
        print(f"Falling back to a random meal: {random_meal_name}.")
        return get_meal_details(random_meal_name)
    
    print(f"Failed to retrieve a meal for category: {category or 'Any'} after {retries} attempts.")
    return None

def main():
    age = int(input("Enter your age: "))
    height = float(input("Enter your height in cm: "))
    weight = float(input("Enter your weight in kg: "))
    gender = input("Enter your gender (male/female): ")
    goal = input("Do you want to gain, lose, or maintain weight? ").strip().lower()
    activity_level = int(input("Enter your activity level (1-5):\n"
                               "1: Sedentary (little or no exercise)\n"
                               "2: Lightly active (light exercise/sports 1-3 days/week)\n"
                               "3: Moderately active (moderate exercise/sports 3-5 days/week)\n"
                               "4: Very active (hard exercise/sports 6-7 days a week)\n"
                               "5: Super active (very hard exercise/sports & physical job or 2x training)\n"))

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

    folder_name = datetime.now().strftime("%d-%m-%y")
    os.makedirs(folder_name, exist_ok=True)

    for meal, category in meal_plan.items():
        meal_details = attempt_get_meal(category)
        if meal_details:
            calories = simulate_calories(meal_details)
            total_calories += calories
            meal_details_list.append((meal, meal_details, calories))
            save_meal_to_file(meal_details, f"{folder_name}/{meal}.txt")
        else:
            print(f"Skipping {meal} due to lack of data.")

    if total_calories > target_calories:
        excess_calories = total_calories - target_calories
        while excess_calories > 0 and meal_details_list:
            meal, details, calories = meal_details_list.pop()
            excess_calories -= calories
            total_calories -= calories
            os.remove(f"{folder_name}/{meal}.txt")

    with open(f"{folder_name}/plan.txt", "w") as plan_file:
        plan_file.write(f"Daily Meal Plan (Calories Target: {target_calories:.2f} kcal)\n")
        plan_file.write("========================================\n\n")
        for meal, details, calories in meal_details_list:
            plan_file.write(f"{meal.capitalize()} - {details['strMeal']}: {calories:.2f} kcal\n")
        plan_file.write(f"\nTotal Calories: {total_calories:.2f} kcal\n")
    
    print(f"Meal plan created successfully in the '{folder_name}' folder.")

if __name__ == "__main__":
    main()
