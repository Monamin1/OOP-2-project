from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QDateEdit, QPushButton,
    QListWidget, QHBoxLayout, QVBoxLayout, QMessageBox, QWidget, 
    QRadioButton, QLabel, QMenuBar, QDockWidget, QTextEdit, QListWidget,
    QSizePolicy
    )

from PyQt6.QtCore import Qt, QRect, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont

import sys

class Inventory(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory")    
        self.resize(800, 500)
        self.setup_ui()
    

    def setup_ui(self):
        central = QWidget()
        central.setStyleSheet("background-color: #ffffff;")
        self.setCentralWidget(central)

        title = QLabel("Login")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 45px; color: #000000; ")
        font = QFont("Times New Roman")
        title.setFont(font)

        self.main_layout = QVBoxLayout(central)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        login_layout = QVBoxLayout(central)
        login_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Username_Input = QLineEdit()
        self.Username_Input.setPlaceholderText("Name")
        self.Username_Input.setFixedSize(200, 30)
        self.Username_Input.setStyleSheet("""
            QLineEdit {
                border: none;
                border-bottom: 1px solid #222222;
                background: transparent;
                color: black;
            }
        """)

        self.Password_Input = QLineEdit()
        self.Password_Input.setPlaceholderText("Address")
        self.Password_Input.setFixedSize(200, 30)
        self.Password_Input.setStyleSheet("""
            QLineEdit {
                border: none;
                border-bottom: 1px solid #222222;
                background: transparent;
                color: black;
            }
        """)

        self.Age_Input = QLineEdit()
        self.Age_Input.setPlaceholderText("Age")
        self.Age_Input.setFixedSize(200, 30)
        self.Age_Input.setStyleSheet("""
            QLineEdit {
                border: none;
                border-bottom: 1px solid #222222;
                background: transparent;
                color: black;
            }
        """)

        self.btn_add = QPushButton("Login")
        self.btn_add.setFixedSize(120, 30)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_add)
        btn_widget = QWidget()
        btn_widget.setLayout(btn_layout)
        self.btn_add.setStyleSheet("background: #222222; color: white")


        self.collapse_btn = QPushButton("☰")
        self.collapse_btn.setFixedSize(30,30)
        col_btn_layout = QHBoxLayout()
        col_btn_layout.addWidget(self.collapse_btn)
        self.col_btn_widget = QWidget()
        self.col_btn_widget.setLayout(col_btn_layout)
        col_style = ("""
            QPushButton {
                background: transparent;
                color: #222222;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #888888;
            }
        """)
        self.collapse_btn.setStyleSheet(col_style)

        self.collapse_btn.clicked.connect(self.toggle_panel)


        self.main_layout.addWidget(self.col_btn_widget, alignment=Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addSpacing(40)

        self.main_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addSpacing(20)

        self.main_layout.addLayout(login_layout)
        login_layout.addWidget(self.Username_Input)
        login_layout.addWidget(self.Password_Input)
        login_layout.addWidget(self.Age_Input)

        self.main_layout.addSpacing(20)

        self.main_layout.addWidget(btn_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addSpacing(100)

        self.panel = collapsable_win(self)

    def toggle_panel(self):
        self.panel.toggle()


class collapsable_win(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("background-color: #ffffff; border-right: 1px solid #cccccc; color: #222222;")
        self.setFixedWidth(200)
        self.setGeometry(-200, 0, 200, parent.height())
        self.is_visible = False

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        top_bar_layout = QHBoxLayout(self)
        top_bar_layout.setContentsMargins(25, 25, 25, 25)
        top_bar_layout.addStretch(0)

        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #222222;
                border: none;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #888888;
            }
        """)
        self.close_btn.clicked.connect(self.toggle)
        top_bar_layout.addWidget(self.close_btn)
        
        main_layout.addLayout(top_bar_layout)
        
        #Menu
        menu_items_layout = QVBoxLayout()
        menu_items_layout.setContentsMargins(0, 0, 0, 0)
        menu_items_layout.setSpacing(0)
        
        self.feedback_btn = QPushButton("Feedback")
        self.admin_btn = QPushButton("Admin")
        
        menu_style = """
            QPushButton {
                background: transparent;
                color: #222222;
                border: none;
                text-align: left;
                padding: 10px 25px;
                font-weight: normal;
            }
            QPushButton:hover {
                background-color: #f0f0f0; /* Light gray hover */
            }
        """
        self.feedback_btn.setStyleSheet(menu_style)
        self.admin_btn.setStyleSheet(menu_style)
        
        menu_items_layout.addWidget(self.feedback_btn)
        menu_items_layout.addWidget(self.admin_btn)
        
        main_layout.addLayout(menu_items_layout)
        main_layout.addStretch(1)

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(400)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)

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



       
if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = Inventory()
   window.show()
   sys.exit(app.exec())
