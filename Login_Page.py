from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QDateEdit, QPushButton,
    QListWidget, QHBoxLayout, QVBoxLayout, QMessageBox, QWidget, QRadioButton
    )

from PyQt6.QtCore import Qt, QDate

import sys


class Inventory(QMainWindow):
    def __init__(self):
       super().__init__()
       self.setWindowTitle("Inventory")
       self.resize(700, 600)
       self.setup_ui()
       self.create_menu()
       
    def create_menu(self):
              menu_bar =self.menuBar()          
              file_menu = menu_bar.addMenu("File")
              feedback_action = file_menu.addAction("Feedback")
              admin_action = file_menu.addAction("Admin")
    
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        login_layout = QVBoxLayout(central)
        login_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Username_Input=QLineEdit()
        self.Username_Input.setPlaceholderText("Enter Username")
        self.Username_Input.setFixedSize(150,30)
        self.Password_Input=QLineEdit()
        self.Password_Input.setPlaceholderText("Enter Password")
        self.Password_Input.setFixedSize(150,30)
        self.Age_Input=QLineEdit()
        self.Age_Input.setFixedSize(150,30)
        layout.addLayout(login_layout)
        login_layout.addWidget(self.Username_Input)
        login_layout.addWidget(self.Password_Input)
        login_layout.addWidget(self.Age_Input)
        
       

       
       
       
       
       
if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = Inventory()
   window.show()
   sys.exit(app.exec())
