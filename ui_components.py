from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from PyQt6.QtCore import QRect, QPropertyAnimation, QEasingCurve, Qt


def create_styled_line_edit(placeholder_text):
    """Creates a QLineEdit with a standard style."""
    line_edit = QLineEdit()
    line_edit.setPlaceholderText(placeholder_text)
    line_edit.setFixedSize(200, 30)
    line_edit.setStyleSheet("""
        QLineEdit {
            border: none;
            border-bottom: 1px solid #222222;
            background: transparent;
            color: black;
        }
    """)
    return line_edit

def create_menu_button():
    """Creates the hamburger menu button."""
    collapse_btn = QPushButton("☰")
    collapse_btn.setFixedSize(30, 30)
    collapse_btn.setStyleSheet("""
        QPushButton {
            background: transparent;
            color: #222222;
            border: none;
            font-weight: bold;
            font-size: 16px;
            margin: 5px;
        }
        QPushButton:hover {
            color: #888888;
        }
    """)
    return collapse_btn

class CollapsablePanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("background-color: #ffffff; border-right: 1px solid #cccccc; color: #222222;")
        self.setFixedWidth(200)
        self.setGeometry(-200, 0, 200, parent.height())
        self.is_visible = False

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        top_bar_layout = QHBoxLayout()
        top_bar_layout.setContentsMargins(10, 10, 10, 10)
        top_bar_layout.addStretch()

        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background: transparent; color: #222222; border: none;
                font-size: 20px; font-weight: bold;
            }
            QPushButton:hover { color: #888888; }
        """)
        self.close_btn.clicked.connect(self.toggle)
        top_bar_layout.addWidget(self.close_btn)
        self.main_layout.addLayout(top_bar_layout)

        # Menu items layout
        self.menu_items_layout = QVBoxLayout()
        self.menu_items_layout.setContentsMargins(0, 0, 0, 0)
        self.menu_items_layout.setSpacing(0)
        self.main_layout.addLayout(self.menu_items_layout)

        self.main_layout.addStretch(1)

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(400)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def add_menu_item(self, text, on_click):
        """Adds a button to the menu."""
        button = QPushButton(text)
        button.setStyleSheet("""
            QPushButton {
                background: transparent; color: #222222; border: none;
                text-align: left; padding: 10px 25px; font-weight: normal;
            }
            QPushButton:hover { background-color: #f0f0f0; }
        """)
        button.clicked.connect(on_click)
        self.menu_items_layout.addWidget(button)

    def toggle(self):
        current_width = self.width()
        current_height = self.parent().height()

        if self.is_visible:
            start_rect = QRect(0, 0, current_width, current_height)
            end_rect = QRect(-current_width, 0, current_width, current_height)
        else:
            start_rect = QRect(-current_width, 0, current_width, current_height)
            end_rect = QRect(0, 0, current_width, current_height)

        self.animation.stop()
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.start()

        self.is_visible = not self.is_visible