from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsOpacityEffect, QPushButton
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QPixmap, QFont
import os

def create_startup_splash(parent=None):

    widget = QWidget(parent)
    widget.setFixedSize(800, 500)
    layout = QVBoxLayout(widget)
    layout.addSpacing(100)
    layout.setAlignment(Qt.AlignmentFlag.AlignRight)
    widget.setStyleSheet("background-color: white;")

    logo = QLabel()
    logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_dir, "assets", "startup_logo.png")

    print("Loading splash image from:", image_path)
    pixmap = QPixmap(image_path)

    if pixmap.isNull():
        logo.setText("⚠️ Could not load image.\n" + image_path)
        logo.setStyleSheet("font-size: 16px; color: red;")
    else:
        logo.setPixmap(
            pixmap.scaled(400, 400,
                          Qt.AspectRatioMode.KeepAspectRatio,
                          Qt.TransformationMode.SmoothTransformation)
        )

    layout.addWidget(logo)

    def go_to_next():
        if parent and hasattr(parent, "switch_view"):
            parent.switch_view("mode_select")

    QTimer.singleShot(3000, go_to_next)

    return widget

def create_mode_select_view(parent=None):

    widget = QWidget(parent)
    layout = QVBoxLayout(widget)
    layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(20)

    layout.addSpacing(250)

    widget.setStyleSheet("background-color: white;")

    # Title
    title = QLabel("Hello, select a mode: ")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setFont(QFont("Times New Roman", 22, QFont.Weight.Normal))
    title.setStyleSheet("color: #222;")
    layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignHCenter)

    layout.addSpacing(10)

    # Buttons
    customer_btn = QPushButton("Customer")
    admin_btn = QPushButton("Admin")

    for btn in (customer_btn, admin_btn):
        btn.setFixedSize(200, 50)
        btn.setFont(QFont("Arial"))
        btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #222222;
                border: none;
            }
            QPushButton:hover {
                color: #888888;
            }
        """)

    # Add each button centered horizontally
    layout.addWidget(customer_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
    layout.addWidget(admin_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

    # push remaining space below buttons (keeps them vertically centered-ish)
    layout.addStretch(1)

    customer_btn.clicked.connect(lambda: parent.switch_view("consumer"))
    admin_btn.clicked.connect(lambda: parent.switch_view("admin"))

    return widget

