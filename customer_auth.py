import json
import os

def get_customers_data():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                             'config', 'customers.json')
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_customer(username, password, name, address, age):
    customers = get_customers_data()
    
    # Check if username already exists
    if username in customers:
        return False, "Username already exists"
    
    # Validate name (no numbers)
    if not name or any(char.isdigit() for char in name):
        return False, "Name cannot contain numbers"
    
    # Validate age
    try:
        age_val = int(age)
        if age_val <= 0 or age_val > 110:
            return False, "Age must be between 1 and 110"
    except (ValueError, TypeError):
        return False, "Age must be a valid number"
    
    # Save customer
    customers[username] = {
        "password": password,
        "name": name,
        "address": address,
        "age": age_val
    }
    
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                             'config', 'customers.json')
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    with open(config_path, 'w') as f:
        json.dump(customers, f, indent=2)
    
    return True, "Registration successful"

def verify_customer_login(username, password):
    customers = get_customers_data()
    
    if username not in customers:
        return False, None, "Invalid username or password"
    
    if customers[username]["password"] != password:
        return False, None, "Invalid username or password"
    
    # Return success, profile data
    profile = customers[username].copy()
    profile.pop("password", None)  # Don't return password
    
    return True, profile, "Login successful"
