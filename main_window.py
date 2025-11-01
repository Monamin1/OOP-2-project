from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

from ui_components import CollapsablePanel, create_menu_button
from ui_views import (create_admin_login_widget, create_consumer_login_widget, create_inventory_widget,
                      FeedbackDialog
)
from customer_page import create_customer_page

class MainWindow(QMainWindow):
    def __init__(self, initial_view='consumer'):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(800, 500)

        self.view_creators = {
            'consumer': create_consumer_login_widget,
            'admin': create_admin_login_widget,
            'inventory': create_inventory_widget,
            'customer': create_customer_page,
        }

        self.setup_ui()
        self.switch_view(initial_view)
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                color: #000000;
            }
            QLineEdit, QTextEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #cccccc;
            }
            QPushButton {
                color: #000000;
                background-color: #f7f7f7;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)


    def setup_ui(self):
        # Main container widget
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: #ffffff;")
        self.setCentralWidget(self.central_widget)

        # Main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Collapse button
        self.collapse_btn = create_menu_button()
        self.collapse_btn.clicked.connect(self.toggle_panel)

        # This widget will hold the current view (admin or consumer)
        self.view_container = QWidget()
        self.view_layout = QVBoxLayout(self.view_container)
        self.view_layout.setContentsMargins(0,0,0,0)

        # Add widgets to main layout
        self.main_layout.addWidget(self.collapse_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(self.view_container)

        # Collapsible Panel
        self.panel = CollapsablePanel(self)
        self.panel.add_menu_item("Consumer", lambda: self.switch_view('consumer'))
        self.panel.add_menu_item("Admin", lambda: self.switch_view('admin'))
        #self.panel.add_menu_item("Inventory", lambda: self.switch_view('inventory'))
        self.panel.add_menu_item("Feedback", self.show_feedback)

    def _handle_button_click(self, view_name):
        if self.parent and hasattr(self.parent, "switch_view"):
            self.parent.switch_view(view_name)

        if self.is_visible:
            self.toggle()


    def toggle_panel(self):
        self.panel.toggle()

    def switch_view(self, view_name):
        if view_name in self.view_creators:
            
            for i in reversed(range(self.view_layout.count())):
                widget_to_remove = self.view_layout.itemAt(i).widget()
                if widget_to_remove:
                    widget_to_remove.setParent(None)

            new_view = self.view_creators[view_name](self)
            self.view_layout.addWidget(new_view)

        else:
            print(f"Error: View '{view_name}' not found.")

    def show_feedback(self):

        dialog = FeedbackDialog(self)
        dialog.exec()
