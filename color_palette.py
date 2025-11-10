# Base Colors
PRIMARY_COLOR = "#222222"
SECONDARY_COLOR = "#0078d7"
SUCCESS_COLOR = "#28a745"
DANGER_COLOR = "#dc3545"
WARNING_COLOR = "#ffc107"
INFO_COLOR = "#6c757d"
LIGHT_COLOR = "#f0f0f0"
WHITE_COLOR = "#ffffff"
BLACK_COLOR = "#000000"

# Font Settings
FONT_FAMILY_TITLE = "Times New Roman"
FONT_SIZE_TITLE = "45px"
FONT_SIZE_LARGE = "30px"
FONT_SIZE_MEDIUM = "20px"
FONT_SIZE_NORMAL = "14px"

# Status Colors for Inventory
STOCK_GOOD = SUCCESS_COLOR
STOCK_LOW = WARNING_COLOR
STOCK_CRITICAL = DANGER_COLOR
STOCK_CUSTOM = INFO_COLOR

def get_base_widget_style():
    #widget
    return f"""
        QWidget {{
            background-color: {WHITE_COLOR};
            color: {BLACK_COLOR};
        }}
    """

def get_input_fields_style():
    #QLineEdit and QTextEdit
    return f"""
        QLineEdit, QTextEdit {{
            background-color: {WHITE_COLOR};
            color: {BLACK_COLOR};
            border: 1px solid #cccccc;
        }}
    """

def get_button_base_style():
    # buttons
    return f"""
        QPushButton {{
            color: {BLACK_COLOR};
            background-color: #f7f7f7;
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 4px 8px;
        }}
        QPushButton:hover {{
            background-color: #e0e0e0;
        }}
    """

def get_title_style():
    # main titles
    return f"""
        font-size: {FONT_SIZE_TITLE};
        color: {BLACK_COLOR};
        font-family: {FONT_FAMILY_TITLE};
    """

def get_table_style():
    # QTableWidget
    return f"""
        QTableWidget {{
            background-color: {WHITE_COLOR};
            color: {BLACK_COLOR};
            border: 1px solid #cccccc;
            gridline-color: #e0e0e0;
        }}
        QHeaderView::section {{
            background-color: {LIGHT_COLOR};
            color: {BLACK_COLOR};
            padding: 4px;
            border: 1px solid #cccccc;
            font-size: {FONT_SIZE_NORMAL};
        }}
    """

def get_action_button_style(button_type="primary"):
    styles = {
        "primary": PRIMARY_COLOR,
        "secondary": SECONDARY_COLOR,
        "success": SUCCESS_COLOR,
        "danger": DANGER_COLOR,
        "warning": WARNING_COLOR,
    }
    color = styles.get(button_type, PRIMARY_COLOR)
    
    return f"""
        QPushButton {{
            background: {color};
            color: white;
            border: none;
            border-radius: 5px;
            padding: 6px 12px;
        }}
        QPushButton:hover {{
            background: darker({color}, 110%);
        }}
    """

def get_login_input_style(placeholder_text):
    return f"""
        QLineEdit {{
            padding: 8px;
            margin: 5px;
            border: 1px solid #cccccc;
            border-radius: 4px;
            font-size: {FONT_SIZE_NORMAL};
        }}
        QLineEdit[text=""] {{
            color: #666666;
        }}
    """

def get_card_style():
    return f"""
        QGroupBox {{
            border: 1px solid #ccc;
            border-radius: 8px;
            background: #fafafa;
            padding: 10px;
        }}
    """

# main_window.py
def get_app_style():
    return f"""
        {get_base_widget_style()}
        {get_input_fields_style()}
        {get_button_base_style()}
    """

# ui_views.py
def get_inventory_status_color(quantity):
    if quantity > 15:
        return STOCK_GOOD
    elif quantity >= 5:
        return STOCK_LOW
    else:
        return STOCK_CRITICAL