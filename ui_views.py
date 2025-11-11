from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QHBoxLayout, QComboBox, QLineEdit, 
                             QMessageBox, QDialog, QTextEdit, QProgressBar, QGraphicsDropShadowEffect,
                             QCheckBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPixmap

from ui_components import create_styled_line_edit, CollapsablePanel
from feedback_email import send_feedback_email
from admin_auth import (get_admin_credentials, save_admin_credentials,
                     remember_admin_login, get_remembered_admin, forget_admin_login)
from customer_auth import (get_customers_data, save_customer, verify_customer_login)
import os, json
from persistence import save_file_state, load_file_state, get_save_files

def create_password_toggle_button(password_input):
    toggle_btn = QPushButton("⊙")  # Eye icon
    toggle_btn.setFixedWidth(40)
    toggle_btn.setStyleSheet("""
        QPushButton {
            background: transparent; color: #222; border: none; border-radius: 3px;
        }
        QPushButton:hover { background: #e0e0e0; }
    """)
    
    def toggle_password_visibility():
        if password_input.echoMode() == QLineEdit.EchoMode.Password:
            password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            toggle_btn.setText("–")  # Closed eye
        else:
            password_input.setEchoMode(QLineEdit.EchoMode.Password)
            toggle_btn.setText("⊙")  # Open eye
    
    toggle_btn.clicked.connect(toggle_password_visibility)
    return toggle_btn

def _create_base_login_widget():
    view_widget = QWidget()
    layout = QVBoxLayout(view_widget)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.setContentsMargins(20, 20, 20, 20)
    return view_widget, layout

def set_login_background(view_widget):
    """Set background_photo.png with semi-transparent overlay so widgets remain visible."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    bg_path = os.path.join(base_dir, "assets", "background_photo.png")
    
    if os.path.exists(bg_path):
        # Use stylesheet with semi-transparent background instead of palette
        # This allows widgets to render on top properly
        view_widget.setStyleSheet(f"""
            QWidget {{
                background-image: url("{bg_path}");
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                background-color: rgba(255, 255, 255, 0.7);
            }}
        """)

def create_customer_login_widget(parent=None):
    view_widget, layout = _create_base_login_widget()
    
    # Apply background image
    set_login_background(view_widget)

    #title
    title = QLabel("Login")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setStyleSheet("font-size: 45px; color: #000000;")
    title.setFont(QFont("Times New Roman"))

    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    title.setContentsMargins(0, 0, 0, 0)

    shadow_effect = QGraphicsDropShadowEffect()
    shadow_effect.setBlurRadius(30)
    shadow_effect.setColor(QColor(50,50,50,180))
    shadow_effect.setOffset(4, 4)
    title.setGraphicsEffect(shadow_effect)


    #customer_label
    customer_label = QLabel("Customer")
    customer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    customer_label.setStyleSheet("font-size: 18px; color: #000000;")
    customer_label.setFont(QFont("Times New Roman"))
    customer_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    customer_label.setContentsMargins(0, 0, 0, 0)

    shadow_effect = QGraphicsDropShadowEffect()
    shadow_effect.setBlurRadius(30)
    shadow_effect.setColor(QColor(50,50,50,180))
    shadow_effect.setOffset(4, 4)
    customer_label.setGraphicsEffect(shadow_effect)


    username_input = create_styled_line_edit("Username")
    username_input.setFixedWidth(200)
    password_input = create_styled_line_edit("Password")
    username_input.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    password_input.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    password_input.setEchoMode(QLineEdit.EchoMode.Password)
    
    password_toggle_btn = create_password_toggle_button(password_input)
    username_layout = QHBoxLayout()
    password_layout = QHBoxLayout()
    username_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
    password_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

    fields_widget = QWidget()
    fields_widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    fields_widget.setStyleSheet("background: transparent;")
    fields_layout = QVBoxLayout(fields_widget)
    fields_layout.setContentsMargins(0, 0, 0, 0)
    fields_layout.setSpacing(10)
    fields_widget.setFixedWidth(260)


    username_layout.addWidget(username_input)
    password_layout.addWidget(password_input)
    password_layout.addWidget(password_toggle_btn)

    fields_layout.addLayout(username_layout)
    fields_layout.addLayout(password_layout)

    login_btn = QPushButton("Login")
    login_btn.setFixedSize(120, 30)
    login_btn.setStyleSheet("background: #222222; color: white; border-radius: 5px;")
    
    register_btn = QPushButton("Register")
    register_btn.setFixedSize(120, 30)
    register_btn.setStyleSheet("background: #0078d7; color: white; border-radius: 5px;")
    
    # Connect Enter key to trigger login for username and password fields
    username_input.returnPressed.connect(login_btn.click)
    password_input.returnPressed.connect(login_btn.click)

    def handle_customer_login():
        username = username_input.text()
        password = password_input.text()

        if not username or not password:
            QMessageBox.warning(view_widget, "Missing Info", "Please enter username and password.")
            return

        success, profile, message = verify_customer_login(username, password)
        if success:
            if parent:
                parent.active_user = {
                    "username": username,
                    "name": profile["name"],
                    "address": profile["address"],
                    "age": profile["age"]
                }
                print("✅ Logged in customer:", parent.active_user)

            if hasattr(parent, "switch_view"):
                parent.switch_view("customer_catalog")
        else:
            msg_box = QMessageBox(view_widget)
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setText(message)
            msg_box.setWindowTitle("Login Failed")
            msg_box.exec()

    def show_registration_dialog():
        dialog = QDialog(view_widget)
        dialog.setWindowTitle("Register")
        dialog.setFixedWidth(350)
        
        dlg_layout = QVBoxLayout(dialog)
        dlg_layout.setSpacing(10)
        
        # Username
        reg_username = QLineEdit(dialog)
        reg_username.setPlaceholderText("Username")
        dlg_layout.addWidget(reg_username)
        
        # Password
        reg_password = QLineEdit(dialog)
        reg_password.setPlaceholderText("Password")
        reg_password.setEchoMode(QLineEdit.EchoMode.Password)
        reg_password_toggle = create_password_toggle_button(reg_password)
        reg_password_layout = QHBoxLayout()
        reg_password_layout.addWidget(reg_password)
        reg_password_layout.addWidget(reg_password_toggle)
        dlg_layout.addLayout(reg_password_layout)

        # Confirm Password
        reg_password_confirm = QLineEdit(dialog)
        reg_password_confirm.setPlaceholderText("Confirm Password")
        reg_password_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        reg_password_confirm_toggle = create_password_toggle_button(reg_password_confirm)
        reg_password_confirm_layout = QHBoxLayout()
        reg_password_confirm_layout.addWidget(reg_password_confirm)
        reg_password_confirm_layout.addWidget(reg_password_confirm_toggle)
        dlg_layout.addLayout(reg_password_confirm_layout)
        
        # Name
        reg_name = QLineEdit(dialog)
        reg_name.setPlaceholderText("Full Name")
        dlg_layout.addWidget(reg_name)
        
        # Address
        reg_address = QLineEdit(dialog)
        reg_address.setPlaceholderText("Address")
        dlg_layout.addWidget(reg_address)
        
        # Age
        reg_age = QLineEdit(dialog)
        reg_age.setPlaceholderText("Age")
        dlg_layout.addWidget(reg_age)
        
        # Register button
        register_confirm_btn = QPushButton("Register")
        register_confirm_btn.setStyleSheet("background: #28a745; color: white; border-radius: 5px; padding: 5px;")
        dlg_layout.addWidget(register_confirm_btn)
        
        def handle_registration():
            username = reg_username.text().strip()
            password = reg_password.text().strip()
            confirm = reg_password_confirm.text().strip()
            name = reg_name.text().strip()
            address = reg_address.text().strip()
            age = reg_age.text().strip()
            
            # Validation
            if not username or not password or not name or not address or not age:
                QMessageBox.warning(dialog, "Missing Info", "Please fill in all fields.")
                return
            
            if not password or len(password) < 4:
                QMessageBox.warning(dialog, "Weak Password", "Password must be at least 4 characters.")
                return

            # Confirm password matches
            if password != confirm:
                QMessageBox.warning(dialog, "Password Mismatch", "Password and confirmation do not match.")
                return
            
            # Validate name (no numbers)
            if any(char.isdigit() for char in name):
                QMessageBox.warning(dialog, "Invalid Name", "Name cannot contain numbers.")
                return
            
            # Validate age
            try:
                age_val = int(age)
                if age_val <= 0 or age_val > 110:
                    QMessageBox.warning(dialog, "Invalid Age", "Age must be between 1 and 110.")
                    return
            except (ValueError, TypeError):
                QMessageBox.warning(dialog, "Invalid Age", "Age must be a valid number.")
                return
            
            # Try to register
            success, msg = save_customer(username, password, name, address, age)
            if success:
                QMessageBox.information(dialog, "Success", "Registration successful! You can now login.")
                dialog.accept()
            else:
                QMessageBox.warning(dialog, "Registration Failed", msg)
        
        register_confirm_btn.clicked.connect(handle_registration)
        
        dialog.exec()

    login_btn.clicked.connect(handle_customer_login)
    register_btn.clicked.connect(show_registration_dialog)

    layout.addStretch(1)

    icon_label = QLabel()
    icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    # Make the label transparent so PNG transparency shows through
    icon_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir, "assets", "login_icon.png")

    pixmap = QPixmap(icon_path)

    if not pixmap.isNull():
        icon_label.setPixmap(
            pixmap.scaled(80, 80,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation)
        )
    layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)

    layout.addSpacing(10)
    layout.addWidget(title)
    layout.addWidget(customer_label, alignment=Qt.AlignmentFlag.AlignCenter)
    layout.addSpacing(20)
    layout.addWidget(fields_widget, alignment=Qt.AlignmentFlag.AlignCenter)
    layout.addSpacing(20)
    
    # Login and Register buttons side by side
    button_layout = QHBoxLayout()
    button_layout.addStretch()
    button_layout.addWidget(login_btn)
    button_layout.addWidget(register_btn)
    button_layout.addStretch()
    layout.addLayout(button_layout)
    
    layout.addSpacing(20)
    layout.addStretch(1)

    return view_widget

def create_inventory_widget(main_window):
    view_widget = QWidget()
    layout = QVBoxLayout(view_widget)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(15)

    title = QLabel("Inventory")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setStyleSheet("font-size: 45px; color: #000000;")
    title.setFont(QFont("Times New Roman"))
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    title.setContentsMargins(0, 0, 0, 0)

    shadow_effect = QGraphicsDropShadowEffect()
    shadow_effect.setBlurRadius(30)
    shadow_effect.setColor(QColor(50,50,50,180))
    shadow_effect.setOffset(4, 4)
    title.setGraphicsEffect(shadow_effect)

    icon_label = QLabel()
    icon_label.setAlignment(Qt.AlignmentFlag.AlignRight)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir, "assets", "login_icon.png")

    pixmap = QPixmap(icon_path)
    if not pixmap.isNull():
        icon_label.setPixmap(
            pixmap.scaled(80, 80,
                          Qt.AspectRatioMode.KeepAspectRatio,
                          Qt.TransformationMode.SmoothTransformation)
        )

    #inventory table
    inventory_table = QTableWidget()
    inventory_table.setColumnCount(4)
    inventory_table.setHorizontalHeaderLabels(["Category", "Product", "Quantity", "Status"])

    header = inventory_table.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    inventory_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    layout.addWidget(inventory_table)

    header = inventory_table.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
    header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
    header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
    header.setSectionResizeMode(3, QHeaderView.ResizeMode.Interactive)

    inventory_table.setStyleSheet("""
        QTableWidget {
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #cccccc;
            gridline-color: #e0e0e0;
            selection-background-color: #0078d7;
            selection-color: white;
            /* Hovered item highlight */
            selection-padding: 2px;
        }
        QTableWidget::item:hover {
            background: #e6f7ff;
        }
        QHeaderView::section {
            background-color: #f0f0f0;
            color: #000000;
            padding: 4px;
            border: 1px solid #cccccc;
            font-size: 14px;
        }
    """)

    def colorize_quantity_item(item):
        try:
            quantity = int(item.text())
        except (ValueError, TypeError):
            item.setBackground(QColor("white"))
            item.setForeground(QColor("black"))
            return "Unknown"

        if quantity > 15:
            item.setBackground(QColor("#28a745"))
            item.setForeground(QColor("white"))
            return "Good"
        elif quantity >= 5:
            item.setBackground(QColor("#ffc107"))
            item.setForeground(QColor("black"))
            return "Low"
        else:
            item.setBackground(QColor("#dc3545"))
            item.setForeground(QColor("white"))
            return "Empty / Critical"

    # orders table
    orders_title = QLabel("Customer Orders")
    orders_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    orders_title.setStyleSheet("font-size: 45px; margin-top: 20px;")
    orders_title.setFont(QFont("Times New Roman"))
    orders_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    orders_title.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    orders_title.setContentsMargins(0, 0, 0, 0)

    shadow_effect = QGraphicsDropShadowEffect()
    shadow_effect.setBlurRadius(30)
    shadow_effect.setColor(QColor(50,50,50,180))
    shadow_effect.setOffset(4, 4)
    orders_title.setGraphicsEffect(shadow_effect)

    orders_table = QTableWidget()
    orders_table.setColumnCount(7)
    orders_table.setHorizontalHeaderLabels(["Buyer", "Address", "Age", "Product", "Quantity", "Total", "Completed"])
    orders_header = orders_table.horizontalHeader()
    orders_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    # Make orders table read-only and behave like inventory table
    orders_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    orders_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    orders_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
    orders_table.setStyleSheet("""
        QTableWidget {
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #cccccc;
            gridline-color: #e0e0e0;
        }
    """)

    def refresh_stocks():
        inventory = getattr(main_window, "inventory_data", {})
        inventory_table.blockSignals(True)
        inventory_table.setRowCount(len(inventory))
        inventory_table.setStyleSheet("""
            QTableWidget { background-color: #ffffff; color: #000; border: 1px solid #ccc; }
            QHeaderView::section { background-color: #f0f0f0; color: #000; font-weight: bold; }
        """)

        for row, (prod_name, info) in enumerate(inventory.items()):
            prod_type = info.get("type", "")
            qty = int(info.get("quantity", 0))

            # Fill cells
            inventory_table.setItem(row, 0, QTableWidgetItem(prod_type))
            inventory_table.setItem(row, 1, QTableWidgetItem(prod_name))
            qty_item = QTableWidgetItem(str(qty))
            inventory_table.setItem(row, 2, qty_item)

            # Determine stock status color
            if "Customized" in prod_name:
                color = QColor("#6c757d")
                status = "Customizable"
            elif qty > 15:
                color = QColor("#28a745")
                status = "Good"
            elif qty >= 5:
                color = QColor("#ffc107")
                status = "Low"
            else:
                color = QColor("#dc3545")
                status = "Critical"

            status_item = QTableWidgetItem(status)
            status_item.setBackground(color)
            status_item.setForeground(QColor("white"))
            # Prevent status cell from being selected so its colors don't get overridden
            try:
                status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            except Exception:
                # Fallback for PyQt versions where ItemFlag bitwise ops differ
                pass
            inventory_table.setItem(row, 3, status_item)

        inventory_table.blockSignals(False)

    def refresh_orders():
        print("refresh_orders called")
        orders = getattr(main_window, "orders", []) or []
        orders_table.setRowCount(len(orders))
        for r, order in enumerate(orders):
            buyer = order.get("buyer", {}) or {}
            it0 = QTableWidgetItem(buyer.get("name", ""))
            it1 = QTableWidgetItem(buyer.get("address", ""))
            it2 = QTableWidgetItem(str(buyer.get("age", "")))
            it3 = QTableWidgetItem(order.get("product", ""))
            it4 = QTableWidgetItem(str(order.get("quantity", "")))
            it5 = QTableWidgetItem(str(order.get("total", "")))
            # Create a checkbox for the "Completed" column
            checkbox = QCheckBox()
            checkbox.setStyleSheet("""
                QCheckBox::indicator {
                    width: 15px;
                    height: 15px;
                    border: 1px solid #888;
                    border-radius: 3px;
                }
                QCheckBox::indicator:checked {
                    background-color: #28a745;
                    border: 1px solid #28a745;
                }
            """)
            # Make order cells non-editable
            for it in (it0, it1, it2, it3, it4, it5):
                try:
                    it.setFlags(it.flags() & ~Qt.ItemFlag.ItemIsEditable)
                except Exception:
                    pass
            orders_table.setItem(r, 0, it0)
            orders_table.setItem(r, 1, it1)
            orders_table.setItem(r, 2, it2)
            orders_table.setItem(r, 3, it3)
            orders_table.setItem(r, 4, it4)
            orders_table.setItem(r, 5, it5)
            # Add checkbox to the "Completed" column and center it
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            checkbox_layout.addWidget(checkbox, alignment=Qt.AlignmentFlag.AlignCenter)
            orders_table.setCellWidget(r, 6, checkbox_widget)

            # When checkbox is toggled, apply strikethrough to the row
            def make_toggle_handler(row_idx):
                def on_checkbox_toggled(checked):
                    for col in range(6):  # Columns 0-5 (not the checkbox column)
                        item = orders_table.item(row_idx, col)
                        if item:
                            if checked:
                                font = item.font()
                                font.setStrikeOut(True)
                                item.setFont(font)
                            else:
                                font = item.font()
                                font.setStrikeOut(False)
                                item.setFont(font)
                return on_checkbox_toggled
            checkbox.stateChanged.connect(make_toggle_handler(r))

    # Buttons
    button_layout = QHBoxLayout()
    button_layout.addStretch()

    refresh_btn = QPushButton("Refresh")
    refresh_btn.setStyleSheet("background: #0078d7; color: white; border-radius: 5px; padding: 5px 10px;")
    refresh_btn.clicked.connect(lambda: refresh_stocks())
    refresh_btn.clicked.connect(lambda: (refresh_stocks(), refresh_orders()))

    save_btn = QPushButton("Save State")
    save_btn.setStyleSheet("background: #28a745; color: white; border-radius: 5px; padding: 5px 10px;")

    load_btn = QPushButton("Load State")
    load_btn.setStyleSheet("background: #6c757d; color: white; border-radius: 5px; padding: 5px 10px;")

    restock_btn = QPushButton("Restock Selected")
    restock_btn.setStyleSheet("background: #28a745; color: white; border-radius: 5px; padding: 5px 10px;")

    button_layout.addWidget(refresh_btn)
    button_layout.addWidget(save_btn)
    button_layout.addWidget(load_btn)
    button_layout.addWidget(restock_btn)

    # Add widgets
    layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(title)
    layout.addWidget(inventory_table)
    layout.addLayout(button_layout)
    layout.addWidget(orders_title)
    layout.addWidget(orders_table)

    # Orders action buttons
    orders_button_layout = QHBoxLayout()
    orders_button_layout.addStretch()
    
    remove_completed_btn = QPushButton("Remove Completed Orders")
    remove_completed_btn.setStyleSheet("background: #dc3545; color: white; border-radius: 5px; padding: 5px 10px;")
    
    def remove_completed_orders():
        # Find all checked rows and remove them
        rows_to_remove = []
        for r in range(orders_table.rowCount()):
            checkbox_widget = orders_table.cellWidget(r, 6)
            if checkbox_widget:
                # Get the checkbox from the widget
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    rows_to_remove.append(r)
        
        if not rows_to_remove:
            QMessageBox.information(view_widget, "No Orders Selected", "No completed orders to remove.")
            return
        
        # Remove orders from main_window.orders in reverse order to avoid index shifting
        orders = getattr(main_window, "orders", []) or []
        for r in sorted(rows_to_remove, reverse=True):
            if r < len(orders):
                orders.pop(r)
        
        refresh_orders()
        QMessageBox.information(view_widget, "Removed", f"Removed {len(rows_to_remove)} completed order(s).")
    
    remove_completed_btn.clicked.connect(remove_completed_orders)
    orders_button_layout.addWidget(remove_completed_btn)
    
    layout.addLayout(orders_button_layout)



    class ChangeCredentialsDialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Change Credentials")
            self.setFixedWidth(350)
            
            layout = QVBoxLayout(self)
            layout.setSpacing(10)
            
            old_username = QLineEdit(self)
            old_username.setPlaceholderText("Current Username")
            old_password = QLineEdit(self)
            old_password.setPlaceholderText("Current Password")
            old_password.setEchoMode(QLineEdit.EchoMode.Password)
            
            # Add toggle button for old password
            old_password_toggle = create_password_toggle_button(old_password)
            old_password_layout = QHBoxLayout()
            old_password_layout.addWidget(old_password)
            old_password_layout.addWidget(old_password_toggle)
            
            new_username = QLineEdit(self)
            new_username.setPlaceholderText("New Username")
            new_password = QLineEdit(self)
            new_password.setPlaceholderText("New Password")
            new_password.setEchoMode(QLineEdit.EchoMode.Password)
            
            # Add toggle button for new password
            new_password_toggle = create_password_toggle_button(new_password)
            new_password_layout = QHBoxLayout()
            new_password_layout.addWidget(new_password)
            new_password_layout.addWidget(new_password_toggle)
            
            save_btn = QPushButton("Save Changes")
            save_btn.setStyleSheet("background: #222222; color: white; border-radius: 5px; padding: 5px;")
            
            def save_changes():
                credentials = get_admin_credentials()
                if credentials.get(old_username.text()) != old_password.text():
                    QMessageBox.warning(self, "Error", "Current credentials are incorrect")
                    return
                
                if not new_username.text() or not new_password.text():
                    QMessageBox.warning(self, "Error", "New credentials cannot be empty")
                    return
                
                # Check if old and new credentials are the same
                if old_username.text() == new_username.text() and old_password.text() == new_password.text():
                    QMessageBox.warning(self, "Error", "New credentials cannot be the same as old credentials")
                    return
                
                try:
                    save_admin_credentials(new_username.text(), new_password.text())
                    QMessageBox.information(self, "Success", "Credentials updated successfully")
                    self.accept()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to update credentials: {str(e)}")
            
            save_btn.clicked.connect(save_changes)
            
            layout.addWidget(old_username)
            layout.addLayout(old_password_layout)
            layout.addWidget(new_username)
            layout.addLayout(new_password_layout)
            layout.addWidget(save_btn)

    # Create settings panel
    settings_panel = CollapsablePanel(view_widget)
    
    def change_credentials():
        dialog = ChangeCredentialsDialog(view_widget)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            main_window.switch_view('admin')
    
    settings_panel.add_menu_item("Change Credentials", change_credentials)
    settings_panel.add_menu_item("Log Out", lambda: main_window.switch_view('admin'))

    settings_btn = QPushButton("☰")
    settings_btn.setFixedSize(30, 30)
    settings_btn.setStyleSheet("""
        QPushButton {
            background: transparent;
            border: none;
            font-size: 20px;
            color: #222222;
        }
        QPushButton:hover {
            color: #666666;
        }
    """)
    settings_btn.clicked.connect(settings_panel.toggle)

    # Add settings button to layout
    title_layout = QHBoxLayout()
    title_layout.addWidget(settings_btn)
    title_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
    layout.insertLayout(1, title_layout)  # Insert after icon but before title

    def restock_selected():
        selected_row = inventory_table.currentRow()
        if selected_row < 0:
            QMessageBox.information(view_widget, "No Selection", "Please select a product to restock.")
            return
        
        prod_name_item = inventory_table.item(selected_row, 1)
        if not prod_name_item:
            return
        
        reply = QMessageBox.question(view_widget, 'Restock Confirmation',
                                     f"Are you sure you want to restock {prod_name_item.text()}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            # Get default quantity for this product type
            inv = main_window.inventory_data
            prod_name = prod_name_item.text()

            if prod_name in inv:
                # Default max quantity for restock
                max_stock = 50
                current_stock = int(inv[prod_name].get("quantity", 0))
                if current_stock >= max_stock:
                    QMessageBox.information(view_widget, "Already Full", f"{prod_name} is already at full stock.")
                    return

                # Restore to default quantity (50) for all product types
                inv[prod_name]["quantity"] = max_stock

                # Update any product cards in the customer view
                if hasattr(main_window, 'product_card_map'):
                    card = main_window.product_card_map.get(prod_name)
                    if card:
                        if hasattr(card, 'buy_btn'):
                            card.buy_btn.setEnabled(True)
                            card.buy_btn.setText("Add to Cart")
                        if hasattr(card, 'name_label'):
                            qty = inv[prod_name]["quantity"]
                            card.name_label.setText(f"{inv[prod_name].get('type', '')}: {prod_name} - {qty} left")

            refresh_stocks()
            QMessageBox.information(view_widget, "Restock Complete", 
                                  f"{prod_name} has been restocked.")

    def save_current_state():
        try:
            filename = save_file_state(
                main_window.inventory_data,
                main_window.orders,
                main_window.active_user,
                main_window.cart_items
            )
            QMessageBox.information(view_widget, "Save Complete",
                                  f"File state saved to:\n{os.path.basename(filename)}")
        except Exception as e:
            QMessageBox.warning(view_widget, "Save Failed",
                              f"Could not save file state:\n{str(e)}")
    
    def load_saved_state():
        try:
            files = get_save_files()
            if not files:
                QMessageBox.information(view_widget, "No Saves",
                                      "No saved files found.")
                return
            
            state = load_file_state(files[0])
            if not state:
                QMessageBox.warning(view_widget, "Load Failed",
                                  "Could not load the save file.")
                return
            
            # Update main window state
            main_window.inventory_data = state['inventory']
            main_window.orders = state['orders']
            if 'cart_items' in state:
                main_window.cart_items = state['cart_items']
            
            refresh_stocks()
            refresh_orders()
            
            QMessageBox.information(view_widget, "Load Complete",
                                  "File state loaded successfully!")
        except Exception as e:
            QMessageBox.warning(view_widget, "Load Failed",
                              f"Error loading file state:\n{str(e)}")

    def on_table_cell_changed(row, column):

        if column == 2:
            item = inventory_table.item(row, column)
            if item:
                # updates the inventory
                inv = getattr(main_window, "inventory_data", None)
                name_item = inventory_table.item(row, 1)
                prod_name = name_item.text() if name_item else None
                try:
                    qty_val = int(item.text())
                except (ValueError, TypeError):
                    qty_val = 0
                if inv is not None and prod_name:
                    inv.setdefault(prod_name, {})["quantity"] = qty_val
                # update status
                status_text = colorize_quantity_item(item)
                inventory_table.setItem(row, 3, QTableWidgetItem(status_text))

    def save_current_state():
        try:
            filename = save_file_state(
                main_window.inventory_data,
                main_window.orders,
                main_window.active_user,
                main_window.cart_items
            )
            QMessageBox.information(view_widget, "Success", f"State saved successfully to:\n{filename}")
        except Exception as e:
            QMessageBox.critical(view_widget, "Error", f"Could not save file state:\n{str(e)}")

    def load_saved_state():
        try:
            state = load_file_state()
            if state:
                main_window.inventory_data = state.get('inventory', {})
                main_window.orders = state.get('orders', [])
                main_window.active_user = state.get('active_user')
                main_window.cart_items = state.get('cart_items', [])
                refresh_stocks()
                refresh_orders()
                QMessageBox.information(view_widget, "Success", "State loaded successfully")
            else:
                QMessageBox.warning(view_widget, "No Save File", "No saved state found")
        except Exception as e:
            QMessageBox.critical(view_widget, "Error", f"Error loading file state:\n{str(e)}")

    restock_btn.clicked.connect(restock_selected)
    save_btn.clicked.connect(save_current_state)
    load_btn.clicked.connect(load_saved_state)
    inventory_table.cellChanged.connect(on_table_cell_changed)

    refresh_stocks()
    refresh_orders()

    return view_widget


def create_admin_login_widget(main_window):
    view_widget, layout = _create_base_login_widget()
    
    # Apply background image
    set_login_background(view_widget)

    #title
    title = QLabel("Login")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setStyleSheet("font-size: 45px; color: #000000;")
    title.setFont(QFont("Times New Roman"))

    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    title.setContentsMargins(0, 0, 0, 0)

    shadow_effect = QGraphicsDropShadowEffect()
    shadow_effect.setBlurRadius(30)
    shadow_effect.setColor(QColor(50,50,50,180))
    shadow_effect.setOffset(4, 4)
    title.setGraphicsEffect(shadow_effect)


    #admin_label
    admin_label = QLabel("Admin")
    admin_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    admin_label.setStyleSheet("font-size: 18px; color: #000000;")
    admin_label.setFont(QFont("Times New Roman"))
    admin_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    admin_label.setContentsMargins(0, 0, 0, 0)

    shadow_effect = QGraphicsDropShadowEffect()
    shadow_effect.setBlurRadius(30)
    shadow_effect.setColor(QColor(50,50,50,180))
    shadow_effect.setOffset(4, 4)
    admin_label.setGraphicsEffect(shadow_effect)


    username_input = create_styled_line_edit("Username")
    password_input = create_styled_line_edit("Password")
    password_input.setEchoMode(QLineEdit.EchoMode.Password)
    
    # Create password toggle button and layout
    password_toggle_btn = create_password_toggle_button(password_input)
    password_layout = QHBoxLayout()
    password_layout.addWidget(password_input)
    password_layout.addWidget(password_toggle_btn)

    # Remember me checkbox
    remember_checkbox = QCheckBox("Remember me")
    remember_checkbox.setStyleSheet("""
        QCheckBox {
            color: #222222;
        }
        QCheckBox::indicator {
            width: 15px;
            height: 15px;
        }
        QCheckBox::indicator:unchecked {
            border: 1px solid #222222;
            background: white;
        }
        QCheckBox::indicator:checked {
            border: 1px solid #222222;
            background: #222222;
        }
    """)

    login_btn = QPushButton("Login")
    login_btn.setFixedSize(120, 30)
    login_btn.setStyleSheet("background: #222222; color: white; border-radius: 5px;")
    
    # Connect Enter key to trigger login for username and password fields
    username_input.returnPressed.connect(login_btn.click)
    password_input.returnPressed.connect(login_btn.click)

    # Check for remembered credentials
    remembered = get_remembered_admin()
    if remembered and remembered.get("username") and remembered.get("password"):
        username_input.setText(remembered["username"])
        password_input.setText(remembered["password"])
        remember_checkbox.setChecked(True)

    def handle_admin_login():
        username = username_input.text()
        password = password_input.text()
        credentials = get_admin_credentials()

        if credentials.get(username) == password:
            if remember_checkbox.isChecked():
                remember_admin_login(username, password)
            else:
                forget_admin_login()
            main_window.switch_view('inventory')
        else:
            msg_box = QMessageBox(view_widget)
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setText("Invalid username or password.")
            msg_box.setWindowTitle("Login Failed")
            msg_box.exec()

    login_btn.clicked.connect(handle_admin_login)

    layout.addStretch(1)

    icon_label = QLabel()
    icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    # Make the label transparent so PNG transparency shows through
    icon_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir, "assets", "login_icon.png")

    pixmap = QPixmap(icon_path)

    if not pixmap.isNull():
        icon_label.setPixmap(
            pixmap.scaled(80, 80,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation)
        )
    layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)

    layout.addSpacing(10)
    layout.addWidget(title)
    layout.addWidget(admin_label, alignment=Qt.AlignmentFlag.AlignCenter)
    layout.addSpacing(20)
    layout.addWidget(username_input)
    layout.addLayout(password_layout)  # Use the layout with toggle button
    layout.addSpacing(20)
    layout.addWidget(login_btn, alignment=Qt.AlignmentFlag.AlignCenter)
    layout.addSpacing(20)
    layout.addWidget(remember_checkbox, alignment=Qt.AlignmentFlag.AlignCenter)
    layout.addStretch(1)

    return view_widget



class FeedbackSender(QThread):
    finished = pyqtSignal(bool, str)

    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def run(self):
        success, error = send_feedback_email(self.message)
        self.finished.emit(success, error)


class FeedbackDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Feedback")
        self.setFixedSize(400, 370)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        label = QLabel("We'd love to hear your feedback:")
        layout.addWidget(label)

        # Name input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Your name")
        self.name_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.name_input)

        # Feedback input
        self.feedback_input = QTextEdit()
        self.feedback_input.setPlaceholderText("Type your feedback here...")
        self.feedback_input.setStyleSheet("""
            QTextEdit {
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.feedback_input)

        # Submit button
        self.submit_btn = QPushButton("Submit")
        self.submit_btn.setStyleSheet("background: #222222; color: white; border-radius: 5px; padding: 5px 10px;")
        self.submit_btn.clicked.connect(self.submit_feedback)
        layout.addWidget(self.submit_btn)

        # Loading overlay
        self.loading_overlay = QWidget(self)
        self.loading_overlay.setGeometry(0, 0, 400, 370)
        self.loading_overlay.setStyleSheet("background-color: rgba(255, 255, 255, 200);")
        overlay_layout = QVBoxLayout(self.loading_overlay)
        overlay_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        loading_label = QLabel("Sending feedback...")
        loading_label.setStyleSheet("font-size: 16px; color: #333; font-weight: bold;")
        overlay_layout.addWidget(loading_label)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        overlay_layout.addWidget(self.progress)

        self.loading_overlay.hide()

    def submit_feedback(self):
        name = self.name_input.text().strip()
        feedback = self.feedback_input.toPlainText().strip()

        if not name:
            QMessageBox.warning(self, "Missing Name", "Please enter your name before submitting.")
            return
        if not feedback:
            QMessageBox.warning(self, "Empty Feedback", "Please enter some feedback before submitting.")
            return

        full_message = f"Reviewer Name: {name}\n\nFeedback:\n{feedback}"

        self.loading_overlay.show()
        self.submit_btn.setEnabled(False)

        self.thread = FeedbackSender(full_message)
        self.thread.finished.connect(self.on_feedback_sent)
        self.thread.start()

    def on_feedback_sent(self, success, error):
        self.loading_overlay.hide()
        self.submit_btn.setEnabled(True)

        if success:
            QMessageBox.information(self, "Thank You", "Your feedback has been sent successfully.")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", f"Failed to send email:\n{error}")
