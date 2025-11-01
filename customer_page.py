from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout,
    QMessageBox, QScrollArea, QGroupBox, QHBoxLayout
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


def create_customer_page(parent=None):
    """Customer marketplace-like page."""
    widget = QWidget(parent)
    layout = QVBoxLayout(widget)
    layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(15)

    # Title
    title = QLabel("🛍️ Customer Marketplace (dipa tapos)")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setStyleSheet("font-size: 28px; font-weight: bold; color: #222;")
    layout.addWidget(title)

    desc = QLabel("Browse our products and place your orders easily below.")
    desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
    desc.setStyleSheet("color: #555; font-size: 14px; margin-bottom: 10px;")
    layout.addWidget(desc)

    # Scroll area for products
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_content = QWidget()
    scroll_layout = QGridLayout(scroll_content)
    scroll_layout.setSpacing(20)
    scroll_layout.setContentsMargins(10, 10, 10, 10)

    # Sample product data (you can later load from DB or CSV)
    products = [
        {"name": "Canvas Tote Bag", "price": 299, "image": "👜"},
        {"name": "Travel Backpack", "price": 799, "image": "🎒"},
        {"name": "Leather Keychain", "price": 149, "image": "🔑"},
        {"name": "Minimalist Purse", "price": 499, "image": "👛"},
    ]

    # Grid layout for products
    row, col = 0, 0
    for product in products:
        card = create_product_card(product, parent)
        scroll_layout.addWidget(card, row, col)
        col += 1
        if col == 3:
            col = 0
            row += 1

    scroll_content.setLayout(scroll_layout)
    scroll_area.setWidget(scroll_content)
    layout.addWidget(scroll_area)

    # Logout button
    logout_btn = QPushButton("Log Out")
    logout_btn.setFixedWidth(120)
    logout_btn.setStyleSheet("""
        QPushButton {
            background: #dc3545; color: white; border: none;
            padding: 6px 12px; border-radius: 5px;
        }
        QPushButton:hover { background: #b02a37; }
    """)
    logout_btn.clicked.connect(lambda: parent.switch_view('consumer'))
    layout.addWidget(logout_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    return widget


def create_product_card(product, parent=None):
    """Creates a single product card with image, name, price, and order button."""
    card = QGroupBox()
    card.setStyleSheet("""
        QGroupBox {
            border: 1px solid #ccc; border-radius: 8px; 
            padding: 10px; background: #fafafa;
        }
        QLabel { color: #333; }
    """)
    layout = QVBoxLayout(card)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # Product "image" (emoji for now)
    img_label = QLabel(product["image"])
    img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    img_label.setStyleSheet("font-size: 48px;")
    layout.addWidget(img_label)

    # Product name
    name_label = QLabel(product["name"])
    name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
    layout.addWidget(name_label)

    # Price
    price_label = QLabel(f"₱{product['price']}")
    price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    price_label.setStyleSheet("font-size: 14px; color: #555;")
    layout.addWidget(price_label)

    # Order button
    order_btn = QPushButton("Place Order")
    order_btn.setStyleSheet("""
        QPushButton {
            background: #28a745; color: white;
            border: none; padding: 6px 12px; border-radius: 5px;
        }
        QPushButton:hover { background: #218838; }
    """)
    order_btn.clicked.connect(lambda: place_order(product, parent))
    layout.addWidget(order_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    return card


def place_order(product, parent=None):
    """Simulate order placement."""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setWindowTitle("Order Placed")
    msg.setText(f"✅ You ordered: {product['name']}\nPrice: ₱{product['price']}\n\nThank you for your purchase!")
    msg.exec()
