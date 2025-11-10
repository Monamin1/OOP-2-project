import json
import os

def get_admin_credentials():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                             'config', 'credentials.json')
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
    except:
        pass
    return {"admin123": "admin123"}

def save_admin_credentials(username, password):
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                             'config', 'credentials.json')
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    creds = {username: password}
    with open(config_path, 'w') as f:
        json.dump(creds, f, indent=2)

def remember_admin_login(username, password):
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                             'config', 'remember.json')
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    with open(config_path, 'w') as f:
        json.dump({
            "remembered_admin": username,
            "remembered_password": password
        }, f)

def get_remembered_admin():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                             'config', 'remember.json')
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                data = json.load(f)
                return {
                    "username": data.get("remembered_admin"),
                    "password": data.get("remembered_password")
                }
    except:
        pass
    return None

def forget_admin_login():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                             'config', 'remember.json')
    if os.path.exists(config_path):
        os.remove(config_path)