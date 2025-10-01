from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QDateEdit, QPushButton,
    QListWidget, QHBoxLayout, QVBoxLayout, QMessageBox, QWidget, 
    QRadioButton, QLabel, QMenuBar
    )

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont

import sys


class Inventory(QMainWindow):
    def __init__(self):
       super().__init__()
       self.setWindowTitle("Inventory")
       self.resize(800, 500)
       self.setup_ui()
       self.create_menu()
       
    def create_menu(self):
              menu_bar =self.menuBar()          
              file_menu = menu_bar.addMenu("File")
              feedback_action = file_menu.addAction("Feedback")
              admin_action = file_menu.addAction("Admin")
    
    def setup_ui(self):
        central = QWidget()
        central.setStyleSheet("background-color: #ffffff;")
        self.setCentralWidget(central)

        title = QLabel("Login")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 45px; color: #000000; ")
        font = QFont("Times New Roman")
        title.setFont(font)

        self.preview = QLabel("Admin")
        self.preview.setFixedSize(60, 30)
        self.preview.setStyleSheet("background: #222222; border-radius: 10px;")
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)

        

        self.main_layout = QVBoxLayout(central)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        login_layout = QVBoxLayout(central)
        login_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Username_Input = QLineEdit()
        self.Username_Input.setPlaceholderText("Username")
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
        self.Password_Input.setPlaceholderText("Password")
        self.Password_Input.setFixedSize(200, 30)
        self.Password_Input.setStyleSheet("""
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
        self.btn_add.setStyleSheet("background: #222222")
        
        

        self.main_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.preview, alignment=Qt.AlignmentFlag.AlignCenter)

        breaker = QLabel("")
        self.main_layout.addWidget(breaker)

        self.main_layout.addLayout(login_layout)
        login_layout.addWidget(self.Username_Input)
        login_layout.addWidget(self.Password_Input)

        breaker2 = QLabel("")
        self.main_layout.addWidget(breaker2)

        self.main_layout.addWidget(btn_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        
       

       
       
       
       
       
if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = Inventory()
   window.show()
   sys.exit(app.exec())
