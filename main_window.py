from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

from ui_components import CollapsablePanel, create_menu_button
from ui_views import (create_admin_login_widget, create_customer_login_widget, create_inventory_widget,
                      FeedbackDialog
)
from customer_page import create_customer_page, create_cart_view
from startup_views import create_startup_splash, create_mode_select_view


class MainWindow(QMainWindow):
    def __init__(self, initial_view='customer'):
        super().__init__()
        self.setWindowTitle("Sisit: Inventory Listing System")
        self.resize(1200, 650)

        self.active_user = None
        self.orders = []
        self.cart_items = []
        self.product_card_map = {}
        self.cart_count_label = None
        self.inventory_data = {
            "CARA": {"type": "Shoulder Bag", "quantity": 50},
            "LIA": {"type": "Shoulder Bag", "quantity": 50},
            "QUI": {"type": "Shoulder Bag", "quantity": 50},
            "ANA": {"type": "Shoulder Bag", "quantity": 50},
            "HYE": {"type": "Shoulder Bag", "quantity": 50},
            "Baby": {"type": "Shoulder Bag", "quantity": 50},
            "BIA": {"type": "Shoulder Bag", "quantity": 50},
            "NYA": {"type": "Sling Bag", "quantity": 50},
            "ORA": {"type": "Sling Bag", "quantity": 50},
            "Normal": {"type": "Tote Bag", "quantity": 50},
            "Large": {"type": "Tote Bag", "quantity": 50},
            "MEG": {"type": "Coin Purse", "quantity": 50},
            "AURA": {"type": "Coin Purse", "quantity": 25},
            "EVA": {"type": "Coin Purse", "quantity": 50},
            "AVA": {"type": "Coin Purse", "quantity": 50},
            "Standard": {"type": "Saddle Bag", "quantity": 50},
}

        self.view_creators = {
            'startup': create_startup_splash,
            'mode_select': create_mode_select_view,
            'customer': create_customer_login_widget,
            'admin': create_admin_login_widget,
            'inventory': create_inventory_widget,
            'customer_catalog': create_customer_page,
            'shopping_cart': create_cart_view,
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

        self.view_container = QWidget()
        self.view_layout = QVBoxLayout(self.view_container)
        self.view_layout.setContentsMargins(0,0,0,0)

        # Add widgets
        self.main_layout.addWidget(self.collapse_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(self.view_container)

        # Collapsible Panel
        self.panel = CollapsablePanel(self)
        self.panel.add_menu_item("Customer", lambda: self.switch_view('customer'))
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

            if view_name in ("customer", "admin"):
                self.collapse_btn.show()
            else:
                self.collapse_btn.hide()
                if self.panel.is_visible:
                    self.panel.toggle()

        else:
            print(f"Error: View '{view_name}' not found.")

    def show_feedback(self):

        dialog = FeedbackDialog(self)
        dialog.exec()

    def update_cart_count(self):
        if self.cart_count_label:
            total_items = sum(item['quantity'] for item in self.cart_items)

            self.cart_count_label.setText(f"({total_items} )")

    def update_product_card_display(self, product_name: str):
        card = self.product_card_map.get(product_name)
        if not card:
            return

        inv = self.inventory_data
        
        if product_name in inv and "Customized" not in product_name:
            current_stock = inv[product_name]["quantity"]
            new_stock_text = f"  —  {current_stock} left" if current_stock > 0 else "  —  Out of Stock"
            
            # Update name_label
            card.name_label.setText(f"{card.product_material}: {card.product_name}{new_stock_text}")
            
            # Update buy_btn state
            if current_stock == 0:
                card.buy_btn.setEnabled(False)
                card.buy_btn.setText("Out of Stock")
            elif not card.buy_btn.isEnabled():
                card.buy_btn.setEnabled(True)
                card.buy_btn.setText("Add to Cart")
