from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QComboBox, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

from ui_components import create_styled_line_edit

def _create_base_login_widget():
    """Creates the base widget and layout for login forms."""
    view_widget = QWidget()
    layout = QVBoxLayout(view_widget)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.setContentsMargins(20, 20, 20, 20)
    return view_widget, layout

def create_consumer_login_widget(main_window):
    """Creates the login widget for the Consumer."""
    view_widget, layout = _create_base_login_widget()

    title = QLabel("Login")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setStyleSheet("font-size: 45px; color: #000000;")
    title.setFont(QFont("Times New Roman"))

    name_input = create_styled_line_edit("Name")
    address_input = create_styled_line_edit("Address")
    age_input = create_styled_line_edit("Age")

    login_btn = QPushButton("Login")
    login_btn.setFixedSize(120, 30)
    login_btn.setStyleSheet("background: #222222; color: white; border-radius: 5px;")

    layout.addSpacing(40)
    layout.addWidget(title)
    layout.addSpacing(20)
    layout.addWidget(name_input)
    layout.addWidget(address_input)
    layout.addWidget(age_input)
    layout.addSpacing(20)
    layout.addWidget(login_btn)
    layout.addStretch()

    return view_widget

def create_inventory_widget(main_window):
    """Creates the inventory view widget with a product table."""
    view_widget = QWidget()
    layout = QVBoxLayout(view_widget)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(15)

    title = QLabel("Inventory")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setStyleSheet("font-size: 45px; color: #000000;")
    title.setFont(QFont("Times New Roman"))

    table = QTableWidget()
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(["Product Type", "Product Name", "Quantity"])
    # Allow interactive resizing but stretch the last column
    header = table.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
    header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
    header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
    table.setStyleSheet("""
        QTableWidget {
            border: 1px solid #cccccc;
            gridline-color: #e0e0e0;
        }
        QHeaderView::section {
            background-color: #f0f0f0;
            padding: 4px;
            border: 1px solid #cccccc;
            font-size: 14px;
        }
    """)

    def format_quantity_cell(row, column):
        """Validates and formats the quantity cell based on its value."""
        if column != 2: # Only act on the Quantity column
            return

        item = table.item(row, column)
        if not item:
            return

        try:
            quantity = int(item.text())
            if quantity > 15:
                item.setBackground(QColor("#28a745"))
            elif quantity >= 5:
                item.setBackground(QColor("#ffc107")) 
            else:
                item.setBackground(QColor("#dc3545")) 
            item.setForeground(QColor("white"))
        except (ValueError, TypeError):
            # If text is not a valid number, reset color and clear text
            item.setBackground(QColor("white"))
            item.setForeground(QColor("black"))
            item.setText("") 

    placeholder_data = [
        ("Tote Bag", "Canvas Tote", "15"),
        ("Backpack", "Travel Backpack", "50"),
        ("Keychain", "Leather Keychain", "200"),
    ]

    product_types = ["Tote Bag", "Backpack", "Purse", "Keychain"]

    table.setRowCount(len(placeholder_data))
    for row, (prod_type, prod_name, quantity) in enumerate(placeholder_data):
        # Add a combobox for the product type column
        combo = QComboBox()
        combo.addItems(product_types)
        combo.setCurrentText(prod_type)
        table.setCellWidget(row, 0, combo)

        table.setItem(row, 1, QTableWidgetItem(prod_name)) 
        quantity_item = QTableWidgetItem(quantity)
        table.setItem(row, 2, quantity_item)
        # Format the initial data
        format_quantity_cell(row, 2)

    # --- Button Section ---
    button_layout = QHBoxLayout()
    button_layout.addStretch()

    add_row_btn = QPushButton("Add Row")
    add_row_btn.setStyleSheet("background: #28a745; color: white; border-radius: 5px; padding: 5px 10px;")

    delete_row_btn = QPushButton("Delete Selected Row")
    delete_row_btn.setStyleSheet("background: #dc3545; color: white; border-radius: 5px; padding: 5px 10px;")

    # Connect cell change signal to format function
    table.cellChanged.connect(format_quantity_cell)


    def add_new_row():
        """Adds a new, empty row to the table for user input."""
        row_position = table.rowCount()
        table.insertRow(row_position)

        combo = QComboBox()
        combo.addItems(product_types)
        table.setCellWidget(row_position, 0, combo)

        table.setItem(row_position, 2, QTableWidgetItem(""))


    def delete_selected_row():
        """Deletes the currently selected row after confirmation."""
        selected_row = table.currentRow()
        if selected_row < 0:
            QMessageBox.information(view_widget, "No Selection", "Please select a row to delete.")
            return

        reply = QMessageBox.question(view_widget, 'Delete Confirmation',
                                     "Are you sure you want to delete this product?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            table.removeRow(selected_row)

    add_row_btn.clicked.connect(add_new_row)
    delete_row_btn.clicked.connect(delete_selected_row)

    button_layout.addWidget(add_row_btn)
    button_layout.addWidget(delete_row_btn)

    layout.addWidget(title)
    layout.addWidget(table)
    layout.addLayout(button_layout)

    return view_widget

def create_admin_login_widget(main_window):
    """Creates the login widget for the Admin."""
    view_widget, layout = _create_base_login_widget()

    title = QLabel("Login")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setStyleSheet("font-size: 45px; color: #000000;")
    title.setFont(QFont("Times New Roman"))

    admin_label = QLabel("Admin")
    admin_label.setFixedSize(60, 30)
    admin_label.setStyleSheet("background: #222222; border-radius: 6px; color: white")
    admin_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    username_input = create_styled_line_edit("Username")
    password_input = create_styled_line_edit("Password")

    login_btn = QPushButton("Login")
    login_btn.setFixedSize(120, 30)
    login_btn.setStyleSheet("background: #222222; color: white; border-radius: 5px;")

    def handle_admin_login():
        """Checks credentials and switches view on success."""
        credentials = {"admin123": "admin123"}
        username = username_input.text()
        password = password_input.text()

        if credentials.get(username) == password:
            main_window.switch_view('inventory')
        else:
            msg_box = QMessageBox(view_widget)
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setText("Invalid username or password.")
            msg_box.setWindowTitle("Login Failed")
            msg_box.exec()

    login_btn.clicked.connect(handle_admin_login)

    layout.addSpacing(20)
    layout.addWidget(title)
    layout.addWidget(admin_label)
    layout.addSpacing(20)
    layout.addWidget(username_input)
    layout.addWidget(password_input)
    layout.addSpacing(20)
    layout.addWidget(login_btn)
    layout.addStretch()

    return view_widget