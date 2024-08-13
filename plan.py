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
        return 1.2  # sedentary 
    elif level == 2:
        return 1.375  # low active
    elif level == 3:
        return 1.55  # medium active
    elif level == 4:
        return 1.725  # very active
    elif level == 5:
        return 1.9  # very very active 
    else:
        raise ValueError("Activity level must be between 1 and 5")

def calculate_daily_calories(bmr, goal, activity_level):
    tdee = bmr * activity_multiplier(activity_level)
    if goal.lower() == 'gain':
        return tdee + 500  # Surplus for weight gain
    elif goal.lower() == 'lose':
        return tdee - 500  # Deficit for weight loss
    elif goal.lower() == 'maintain':
        return tdee  # No change
    else:
        raise ValueError("Goal must be 'gain', 'lose', or 'maintain'")

def main():
    print("Welcome to the BMR and Calorie Calculator!")
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
    
    print(f"\nYour Basal Metabolic Rate (BMR) is: {bmr:.2f} calories/day")
    print(f"To {goal} weight, your recommended daily calorie intake is: {daily_calories:.2f} calories/day")
    
if __name__ == "__main__":
    main()
