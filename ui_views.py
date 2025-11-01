from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QHBoxLayout, QComboBox, QLineEdit, 
                             QMessageBox, QDialog, QTextEdit, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor

from ui_components import create_styled_line_edit
from feedback_email import send_feedback_email

def _create_base_login_widget():
    view_widget = QWidget()
    layout = QVBoxLayout(view_widget)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.setContentsMargins(20, 20, 20, 20)
    return view_widget, layout

def create_consumer_login_widget(parent=None):
    widget = QWidget(parent)
    layout = QVBoxLayout(widget)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    layout.addSpacing(50)
    # Title
    title = QLabel("Login")
    title.setStyleSheet("font-size: 45px; color: #000000;")
    title.setFont(QFont("Times New Roman"))
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        if parent and hasattr(parent, "switch_view"):
            parent.switch_view("customer")

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

    table = QTableWidget()
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(["Product Type", "Product Name", "Quantity"])

    header = table.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
    header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
    header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
    table.setStyleSheet("""
        QTableWidget {
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #cccccc;
            gridline-color: #e0e0e0;
            selection-background-color: #0078d7;
            selection-color: white;
        }
        QHeaderView::section {
            background-color: #f0f0f0;
            color: #000000;
            padding: 4px;
            border: 1px solid #cccccc;
            font-size: 14px;
        }
        QTableWidget QTableCornerButton::section {
            background-color: #f0f0f0;
            border: 1px solid #cccccc;
        }
    """)

    def format_quantity_cell(row, column):
        if column != 2:
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
        combo = QComboBox()
        combo.addItems(product_types)
        combo.setCurrentText(prod_type)
        table.setCellWidget(row, 0, combo)

        table.setItem(row, 1, QTableWidgetItem(prod_name)) 
        quantity_item = QTableWidgetItem(quantity)
        table.setItem(row, 2, quantity_item)
        # Format the initial data
        format_quantity_cell(row, 2)

    # Button Section
    button_layout = QHBoxLayout()
    button_layout.addStretch()

    add_row_btn = QPushButton("Add Row")
    add_row_btn.setStyleSheet("background: #28a745; color: white; border-radius: 5px; padding: 5px 10px;")

    delete_row_btn = QPushButton("Delete Selected Row")
    delete_row_btn.setStyleSheet("background: #dc3545; color: white; border-radius: 5px; padding: 5px 10px;")

    # Connect cell change signal to format function
    table.cellChanged.connect(format_quantity_cell)


    def add_new_row():
        row_position = table.rowCount()
        table.insertRow(row_position)

        combo = QComboBox()
        combo.addItems(product_types)
        table.setCellWidget(row_position, 0, combo)

        table.setItem(row_position, 2, QTableWidgetItem(""))


    def delete_selected_row():
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
