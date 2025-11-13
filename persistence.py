import json
import os
from datetime import datetime

SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'save_files')

def ensure_save_dir():

    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

def save_file_state(inventory_data, orders, active_user=None, cart_items=None):

    ensure_save_dir()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(SAVE_DIR, f'file_state_{timestamp}.json')
    
    state = {
        'inventory': inventory_data,
        'orders': orders,
        'active_user': active_user,
        'cart_items': cart_items or [],
        'saved_at': timestamp
    }
    
    with open(filename, 'w') as f:
        json.dump(state, f, indent=2)
    return filename

def get_save_files():
    ensure_save_dir()
    files = []
    for f in os.listdir(SAVE_DIR):
        if f.startswith('file_state_') and f.endswith('.json'):
            path = os.path.join(SAVE_DIR, f)
            timestamp = os.path.getmtime(path)
            files.append((path, timestamp))
    return [f[0] for f in sorted(files, key=lambda x: x[1], reverse=True)]

def load_file_state(filepath=None):
    ensure_save_dir()
    if not filepath:
        saves = get_save_files()
        if not saves:
            return None
        filepath = saves[0]
    
    try:
        with open(filepath, 'r') as f:
            state = json.load(f)
        return state
    except (json.JSONDecodeError, FileNotFoundError):
        return None

def get_initial_inventory():
    state = load_file_state()
    if state and 'inventory' in state:
        return state['inventory']
    
    return {
        "CARA": {"type": "Shoulder Bag", "quantity": 50},
        "LIA": {"type": "Shoulder Bag", "quantity": 50},
        "QUI": {"type": "Shoulder Bag", "quantity": 50},
        "ANA": {"type": "Shoulder Bag", "quantity": 50},
        "HYE": {"type": "Shoulder Bag", "quantity": 50},
        "BABY": {"type": "Shoulder Bag", "quantity": 50},
        "BIA": {"type": "Shoulder Bag", "quantity": 50},
        "NYA": {"type": "Sling Bag", "quantity": 50},
        "ORA": {"type": "Sling Bag", "quantity": 50},
        "NORMAL": {"type": "Tote Bag", "quantity": 50},
        "LARGE": {"type": "Tote Bag", "quantity": 50},
        "MEG": {"type": "Coin Purse", "quantity": 50},
        "AURA": {"type": "Coin Purse", "quantity": 50},
        "EVA": {"type": "Coin Purse", "quantity": 50},
        "AVA": {"type": "Coin Purse", "quantity": 50},
        "STANDARD": {"type": "Saddle Bag", "quantity": 50},
    }

