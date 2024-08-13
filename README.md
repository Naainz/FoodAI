# FoodAI Project

## Overview

FoodAI is a comprehensive project that combines several tools and functionalities to enhance meal planning, recipe generation, and ingredient analysis. This project consists of two main parts: a standalone set of Python scripts and a Flask web application that acts as an additional, user-friendly interface for some of the functionalities.

## Project Structure

### Non-Flask Scripts

These scripts are designed to run independently from the Flask web application. Each script has a specific purpose related to food and nutrition.

1. **main.py**:
   - **Purpose**: Generates meals based on a list of available ingredients provided by the user.
   - **How it Works**: The user inputs a comma-separated list of ingredients, and the script fetches possible recipes that match at least 50% of the provided ingredients.
   
2. **yolo.py**:
   - **Purpose**: Uses a YOLOv8 model to detect ingredients from an image and suggests recipes based on the detected ingredients.
   - **How it Works**: The script processes an image, identifies ingredients, and then searches for recipes that match those ingredients. Detected ingredients are displayed and saved in an image file.

3. **allergy.py**:
   - **Purpose**: Checks for common allergens in the ingredients of a recipe.
   - **How it Works**: The user provides a recipe name, and the script checks the ingredients for common allergens, then saves the results to a file.

4. **nutrition.py**:
   - **Purpose**: Provides a nutritional breakdown of a recipe based on its ingredients.
   - **How it Works**: The user inputs a recipe name, and the script calculates the nutritional information using a predefined nutritional database, then saves the results to a file.

5. **plan.py**:
   - **Purpose**: Generates a meal plan based on the user's age, weight, height, gender, activity level, and goal (e.g., lose weight, gain weight).
   - **How it Works**: The script calculates the user's Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE) and creates a meal plan that meets the target calorie intake. The meal plan is saved to a file.

6. **recipe.py**:
   - **Purpose**: Fetches and saves the details of a specific recipe.
   - **How it Works**: The user inputs a recipe name, and the script retrieves the recipe's ingredients and instructions, saving them to a file.

### Flask Web Application

The Flask web application provides a user-friendly interface for several functionalities of the project. This is an optional side application that complements the standalone scripts.

#### Available Routes

1. **`/` (Home)**:
   - A simple homepage that introduces the user to the available functionalities.

2. **`/main`**:
   - Allows the user to input a list of ingredients and generates matching recipes. 

3. **`/yolo`**:
   - Users can upload an image, and the application will detect ingredients using YOLO, then suggest recipes based on the detected ingredients.

4. **`/allergy`**:
   - Users can input a recipe name, and the application will check for common allergens in the ingredients.

5. **`/nutrition`**:
   - Allows the user to input a recipe name and receive a nutritional breakdown based on the recipe's ingredients.

6. **`/plan`**:
   - Generates a personalized meal plan based on user input (age, weight, height, gender, activity level, and goal). The plan is displayed on the webpage.

7. **`/recipe`**:
   - Users can input a recipe name to get the details of the recipe, including ingredients and instructions. The ingredients are displayed as cards with thumbnail images.

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installing Required Libraries

```bash
pip install Flask requests ultralytics werkzeug
```

### Running the standalone scripts
Each script can be run individually using Python. For example:
```bash
python main.py
```

### Running the Flask Web Application
To start the Flask web application, run the following command in the terminal:
```bash
python web.py
```
This will start the Flask server, and you can access the application by visiting `http://127.0.0.1:5000/` in your web browser.

## Project features
- **Ingredient-Based Recipe Generation**: Generate recipes based on a list of available ingredients.
- **Image-Based Ingredient Detection**: Detect ingredients from an image and suggest recipes based on the detected ingredients.
- **Allergen Checker**: Check for common allergens in a recipe.
- **Nutritional Information**: Get a nutritional breakdown of a recipe based on its ingredients.
- **Personalized Meal Planning**: Generate a meal plan based on user input (age, weight
- **Recipe Details**: Fetch and display the details of a specific recipe, including ingredients and instructions.

## Acknowledgements
- [YOLOv8](https://github.com/ultralytics/ultralytics)
- [TheMealDB](https://www.themealdb.com/)

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

### DISCLAIMER
This project is for educational purposes only and should not be used as a substitute for professional medical or nutritional advice. Always consult a healthcare provider or nutritionist for personalized advice. None of the information generated by this project should be considered as medical or nutritional advice, and the developers are not liable for any consequences resulting from the use of this project.

---

This README file was written by **AI**. Please acknowledge that this README file may have errors. If you have any questions, please contact me at [s@naai.nz](mailto:s@naai.nz).