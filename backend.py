from datetime import datetime, time, timedelta

def filter_meal(meal, allergies, dietary):
    # Lowercase and split for easy matching
    meal_lower = meal.lower()
    allergy_list = [a.strip().lower() for a in allergies.split(',')] if allergies else []
    dietary = (dietary or '').lower()
    # Allergy filter
    for allergen in allergy_list:
        if allergen and allergen in meal_lower:
            return None  # Exclude this meal
    # Dietary filter
    if 'vegan' in dietary:
        # Exclude meals with egg, cheese, yogurt, milk, meat, fish, chicken, etc.
        for forbidden in ['egg', 'cheese', 'yogurt', 'milk', 'meat', 'fish', 'chicken', 'beef', 'pork', 'seafood', 'honey', 'butter']:
            if forbidden in meal_lower:
                return None
    elif 'vegetarian' in dietary:
        for forbidden in ['meat', 'fish', 'chicken', 'beef', 'pork', 'seafood']:
            if forbidden in meal_lower:
                return None
    if 'no dairy' in dietary or 'dairy-free' in dietary:
        for forbidden in ['cheese', 'yogurt', 'milk', 'butter']:
            if forbidden in meal_lower:
                return None
    if 'gluten' in allergy_list or 'gluten-free' in dietary:
        for forbidden in ['bread', 'pasta', 'spaghetti', 'bun', 'wrap', 'tortilla', 'noodle', 'crouton', 'pizza', 'pretzel', 'bagel']:
            if forbidden in meal_lower:
                return None
    return meal

def generate_routine(user):
    # Only include activities selected by the user
    selected = user.get('selected_activities', [
        'Morning Exercise', 'Breakfast', 'Work Block', 'Lunch', 'Break/Walk', 'Dinner'
    ])
    allergies = user.get('allergies', '')
    dietary = user.get('dietary', '')
    # Meal options for each meal
    meal_options = {
        'Breakfast': ["Oatmeal & fruit", "Peanut butter toast", "Yogurt parfait", "Egg sandwich", "Vegan smoothie", "Bagel & cream cheese"],
        'Lunch': ["Salad & protein", "Chicken wrap", "Grilled cheese sandwich", "Vegan bowl", "Quinoa salad", "Pasta primavera"],
        'Dinner': ["Grilled veggies & rice", "Chicken curry", "Beef stir fry", "Vegan chili", "Paneer tikka", "Fish tacos"]
    }
    import random
    routine = []
    if 'Morning Exercise' in selected:
        routine.append({'time': user.get('ex_time', time(6,30)).strftime('%I:%M %p'), 'task': 'Morning Exercise', 'type': 'exercise', 'details': '30 min jog'})
    if 'Breakfast' in selected:
        # Filter and pick a meal
        meals = [m for m in meal_options['Breakfast'] if filter_meal(m, allergies, dietary)]
        meal = random.choice(meals) if meals else "Fruit bowl"
        routine.append({'time': user.get('bf_time', time(8,0)).strftime('%I:%M %p'), 'task': 'Breakfast', 'type': 'meal', 'details': meal})
    if 'Work Block' in selected:
        routine.append({'time': user.get('work_time', time(9,0)).strftime('%I:%M %p'), 'task': 'Work Block', 'type': 'work', 'details': 'Focus work'})
    if 'Lunch' in selected:
        meals = [m for m in meal_options['Lunch'] if filter_meal(m, allergies, dietary)]
        meal = random.choice(meals) if meals else "Mixed veggie salad"
        routine.append({'time': user.get('lunch_time', time(13,0)).strftime('%I:%M %p'), 'task': 'Lunch', 'type': 'meal', 'details': meal})
    if 'Break/Walk' in selected:
        routine.append({'time': user.get('walk_time', time(16,0)).strftime('%I:%M %p'), 'task': 'Break/Walk', 'type': 'exercise', 'details': '10 min walk'})
    if 'Dinner' in selected:
        meals = [m for m in meal_options['Dinner'] if filter_meal(m, allergies, dietary)]
        meal = random.choice(meals) if meals else "Stir-fried vegetables"
        routine.append({'time': user.get('dinner_time', time(19,0)).strftime('%I:%M %p'), 'task': 'Dinner', 'type': 'meal', 'details': meal})
    return routine

def adapt_schedule(item):
    # Reschedule to one hour after the original scheduled time, not current time
    from datetime import datetime, timedelta
    # Parse the item's time (e.g., '06:30 AM')
    try:
        orig_time = datetime.strptime(item['time'], '%I:%M %p')
    except Exception:
        # fallback: use current time
        orig_time = datetime.now()
    new_time = (orig_time + timedelta(hours=1)).strftime('%I:%M %p')
    return new_time
