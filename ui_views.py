from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QHBoxLayout, QComboBox, QLineEdit, 
                             QMessageBox, QDialog, QTextEdit, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPixmap

from ui_components import create_styled_line_edit
from feedback_email import send_feedback_email
from color_palette import get_table_style, get_title_style, FONT_FAMILY_TITLE
import os

def _create_base_login_widget():
    view_widget = QWidget()
    layout = QVBoxLayout(view_widget)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.setContentsMargins(20, 20, 20, 20)
    return view_widget, layout

def create_customer_login_widget(parent=None):
    widget = QWidget(parent)
    layout = QVBoxLayout(widget)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    layout.addSpacing(50)
    # Title
    title = QLabel("Login")
    title.setStyleSheet(get_title_style())
    title.setFont(QFont(FONT_FAMILY_TITLE))
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)

    icon_label = QLabel()
    icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

    layout.addSpacing(20)

    name_input = create_styled_line_edit("Name")
    layout.addWidget(name_input)
    address_input = create_styled_line_edit("Address")
    layout.addWidget(address_input)
    age_input = create_styled_line_edit("Age")
    layout.addWidget(age_input)

    layout.addSpacing(20)

    # Login button
    login_button = QPushButton("Login")
    login_button.setFixedSize(120, 30)
    login_button.setStyleSheet("background: #222222; color: white; border-radius: 5px;")
    layout.addWidget(login_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def handle_login():
        name = name_input.text().strip()
        address = address_input.text().strip()
        age = age_input.text().strip()

        if not name or not address or not age:
            QMessageBox.warning(widget, "Missing Info", "Please fill in all fields.")
            return

        # Store login info in main window
        if parent:
            parent.active_user = {
                "name": name,
                "address": address,
                "age": age
            }
            print("✅ Logged in user:", parent.active_user)

        # Switch to customer page
        if hasattr(parent, "switch_view"):
            parent.switch_view("customer_catalog")

    login_button.clicked.connect(handle_login)

    return widget

def create_inventory_widget(main_window):
    view_widget = QWidget()
    layout = QVBoxLayout(view_widget)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(15)

    title = QLabel("Inventory")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setStyleSheet("font-size: 45px; color: #000000;")
    title.setFont(QFont("Times New Roman"))

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

    inventory_table.setStyleSheet(get_table_style())

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

    orders_table = QTableWidget()
    orders_table.setColumnCount(6)
    orders_table.setHorizontalHeaderLabels(["Buyer", "Address", "Age", "Product", "Quantity", "Total"])
    orders_header = orders_table.horizontalHeader()
    orders_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
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
            inventory_table.setItem(row, 3, status_item)

        inventory_table.blockSignals(False)

    def refresh_orders():
        print("refresh_orders called")
        orders = getattr(main_window, "orders", []) or []
        orders_table.setRowCount(len(orders))
        for r, order in enumerate(orders):
            buyer = order.get("buyer", {}) or {}
            orders_table.setItem(r, 0, QTableWidgetItem(buyer.get("name", "")))
            orders_table.setItem(r, 1, QTableWidgetItem(buyer.get("address", "")))
            orders_table.setItem(r, 2, QTableWidgetItem(str(buyer.get("age", ""))))
            orders_table.setItem(r, 3, QTableWidgetItem(order.get("product", "")))
            orders_table.setItem(r, 4, QTableWidgetItem(str(order.get("quantity", ""))))
            orders_table.setItem(r, 5, QTableWidgetItem(str(order.get("total", ""))))

    # Buttons
    button_layout = QHBoxLayout()
    button_layout.addStretch()

    refresh_btn = QPushButton("Refresh")
    refresh_btn.setStyleSheet("background: #0078d7; color: white; border-radius: 5px; padding: 5px 10px;")
    refresh_btn.clicked.connect(lambda: refresh_stocks())
    refresh_btn.clicked.connect(lambda: (refresh_stocks(), refresh_orders()))

    add_row_btn = QPushButton("Add Row")
    add_row_btn.setStyleSheet("background: #28a745; color: white; border-radius: 5px; padding: 5px 10px;")

    delete_row_btn = QPushButton("Delete Selected Row")
    delete_row_btn.setStyleSheet("background: #dc3545; color: white; border-radius: 5px; padding: 5px 10px;")

    button_layout.addWidget(refresh_btn)
    button_layout.addWidget(add_row_btn)
    button_layout.addWidget(delete_row_btn)

    # Add widgets
    layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(title)
    layout.addWidget(inventory_table)
    layout.addLayout(button_layout)
    layout.addWidget(orders_title)
    layout.addWidget(orders_table)



    logout_btn = QPushButton("Log Out")
    logout_btn.setFixedWidth(120)
    logout_btn.setStyleSheet("""
        QPushButton {
            background: #dc3545; color: white;
            border: none; border-radius: 5px;
            padding: 6px 12px;
        }
        QPushButton:hover { background: #b02a37; }
    """)
    logout_btn.clicked.connect(lambda: main_window.switch_view('admin'))
    layout.addWidget(logout_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    # Connecting/ calls
    def add_new_row():
        row_position = inventory_table.rowCount()
        inventory_table.insertRow(row_position)
        inventory_table.setItem(row_position, 0, QTableWidgetItem(""))  # type
        inventory_table.setItem(row_position, 1, QTableWidgetItem(""))  # name
        inventory_table.setItem(row_position, 2, QTableWidgetItem("0"))  # qty
        inventory_table.setItem(row_position, 3, QTableWidgetItem("Unknown"))

    def delete_selected_row():
        selected_row = inventory_table.currentRow()
        if selected_row < 0:
            QMessageBox.information(view_widget, "No Selection", "Please select a row to delete.")
            return
        reply = QMessageBox.question(view_widget, 'Delete Confirmation',
                                     "Are you sure you want to delete this product?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            prod_name_item = inventory_table.item(selected_row, 1)
            if prod_name_item:

                # If main_window.inventory_data exists, remove key
                inv = getattr(main_window, "inventory_data", None)
                if inv and prod_name_item.text() in inv:
                    inv.pop(prod_name_item.text(), None)
            inventory_table.removeRow(selected_row)

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

    #refresh_btn.clicked.connect(lambda: (refresh_stocks(), refresh_orders()))
    add_row_btn.clicked.connect(add_new_row)
    delete_row_btn.clicked.connect(delete_selected_row)
    inventory_table.cellChanged.connect(on_table_cell_changed)

    refresh_stocks()
    refresh_orders()

    return view_widget


def create_admin_login_widget(main_window):
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
    password_input.setEchoMode(QLineEdit.EchoMode.Password)

    login_btn = QPushButton("Login")
    login_btn.setFixedSize(120, 30)
    login_btn.setStyleSheet("background: #222222; color: white; border-radius: 5px;")

    def handle_admin_login():
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

    layout.addSpacing(39)

    icon_label = QLabel()
    icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
    layout.addWidget(password_input)
    layout.addSpacing(20)
    layout.addWidget(login_btn, alignment=Qt.AlignmentFlag.AlignCenter)
    layout.addStretch()

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
