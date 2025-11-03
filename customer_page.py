from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea,
    QGroupBox, QHBoxLayout, QSpinBox, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os


def create_customer_page(parent=None):
    widget = QWidget(parent)
    layout = QVBoxLayout(widget)
    layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(15)

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

    title = QLabel("👜 Product Catalog")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setStyleSheet("font-size: 30px; font-weight: bold; color: #222;")
    layout.addWidget(title)

    desc = QLabel("Select color and quantity for each item, then click Buy to order.")
    desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
    desc.setStyleSheet("color: #555; font-size: 14px; margin-bottom: 10px;")
    layout.addWidget(desc)

    # Scroll area
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    content = QWidget()
    content_layout = QVBoxLayout(content)
    content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    content_layout.setSpacing(20)

    # Product Catalog
    catalog = {
        "Shoulder Bag": [
            {"price": 300, "material": "Crocodile Texture", "name": "CARA", "colors": ["Blue/Pink", "Red/Blue", "Pink/Brown", "Brown/Pink", "Pink/Blue", "Tan/Beige", "Beige/Black", "Blue/Tan", "Black/Red", "Brown/Beige"]},
            {"price": 1800, "material": "Real Leather", "name": "LIA", "colors": ["Brown", "Black", "Tan"]},
            {"price": 1200, "material": "Real Leather", "name": "QUI", "colors": ["Black"]},
            {"price": 350, "material": "Faux Leather", "name": "ANA", "colors": ["Brown", "Taupe", "Lt. Green", "Dark Brown"]},
            {"price": 350, "material": "Faux Leather", "name": "HYE", "colors": ["Gray", "Choco Brown", "Black"]},
            {"price": 300, "material": "Faux Leather", "name": "Baby", "colors": ["Brown"]},
            {"price": 280, "material": "Faux Leather", "name": "BIA", "colors": ["Lt. Green"]},
        ],
        "Sling Bag": [
            {"price": 1000, "material": "Real Leather", "name": "NYA", "colors": ["Tan", "Black"]},
            {"price": 680, "material": "Leather", "name": "ORA", "colors": ["Tan", "Black"]},
        ],
        "Tote Bag": [
            {"price": 1200, "material": "Real Leather", "name": "Normal", "colors": ["Standard"]},
            {"price": 1800, "material": "Real Leather", "name": "Large", "colors": ["Standard"]},
        ],
        "Coin Purse": [
            {"price": 70, "material": "Faux Leather", "name": "MEG", "colors": ["Brown", "Mocca", "Red", "Tan", "R. Blue", "D. Brown"]},
            {"price": 70, "material": "Faux Leather", "name": "AURA", "colors": ["Tan", "Brown G", "Camel", "Taupe", "Red", "Black", "Brown", "Gray"]},
            {"price": 50, "material": "Faux Leather", "name": "EVA", "colors": ["Blue", "Tan", "Old Rose", "Mocca", "Gray", "Red", "Taupe", "Brown", "Camel", "Black"]},
            {"price": 50, "material": "Faux Leather", "name": "AVA", "colors": ["Brown", "Tan", "Red", "Black", "Old Rose", "Mocca", "Taupe", "Beige", "Gray", "Blue", "Lt. Green"]},
        ],
        "Saddle Bag": [
            {"price": "1800", "material": "Faux Leather", "name": "Standard", "colors": ["Standard"]},
            {"price": "5500 - 6000", "material": "Leather", "name": "Customized", "colors": ["Customizable"]},
        ],
    }

    for category, items in catalog.items():
        section_label = QLabel(f"- {category} -")
        section_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #222; margin-top: 10px;")
        content_layout.addWidget(section_label, alignment=Qt.AlignmentFlag.AlignCenter)

        for item in items:
            card = create_product_card(item)
            content_layout.addWidget(card)

    content_layout.addStretch(1)
    scroll.setWidget(content)
    layout.addWidget(scroll)

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


def create_product_card(product):
    card = QGroupBox()
    card.setStyleSheet("""
        QGroupBox {
            border: 1px solid #ccc; border-radius: 8px;
            background: #fafafa; padding: 10px;
        }
    """)
    layout = QHBoxLayout(card)
    layout.setContentsMargins(15, 5, 15, 5)
    layout.setSpacing(20)

    # Price
    price_label = QLabel(f"{product['price']} php")
    price_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #222;")
    layout.addWidget(price_label, stretch=1)

    # Material and Name
    main = card.parent()
    while main and not hasattr(main, "switch_view"):
        main = main.parent()

    inv = getattr(main, "inventory_data", {}) if main else {}
    stock_text = ""

    # look up stock
    if product["name"] in inv and "Customized" not in product["name"]:
        stock_left = inv[product["name"]]["quantity"]
        stock_text = f"  —  {stock_left} left"
    else:
        stock_text = "  —  Customizable"

    name_label = QLabel(f"{product['material']}: {product['name']}{stock_text}")
    name_label.setStyleSheet("font-size: 14px; color: #333;")
    layout.addWidget(name_label, stretch=2)

    # Color selector
    color_box = QComboBox()
    color_box.addItems(product["colors"])
    color_box.setFixedWidth(140)
    layout.addWidget(color_box)

    # Quantity selector
    qty_spin = QSpinBox()
    qty_spin.setRange(1, 99)
    qty_spin.setValue(1)
    qty_spin.setFixedWidth(60)
    layout.addWidget(qty_spin)

    # Buy button
    buy_btn = QPushButton("Buy")
    buy_btn.setStyleSheet("""
        QPushButton {
            background: #28a745; color: white;
            border: none; padding: 6px 12px; border-radius: 5px;
        }
        QPushButton:hover { background: #218838; }
    """)

    def buy_action():
        qty = qty_spin.value()
        color = color_box.currentText()
        total = calculate_total(product['price'], qty)

        main = card.parent()
        while main and not hasattr(main, "switch_view"):
            main = main.parent()

        if not main:
            QMessageBox.warning(card, "Error", "Cannot find main window.")
            return

        inv = getattr(main, "inventory_data", {})
        product_name = product['name']

        if product_name in inv and "Customized" not in product_name:
            current_stock = inv[product_name]["quantity"]
            if qty > current_stock:
                QMessageBox.warning(
                    card,
                    "Insufficient Stock",
                    f"Only {current_stock} left in stock for {product_name}!"
                )
                return
            # reduce stock
            inv[product_name]["quantity"] = max(0, current_stock - qty)

        # record order
        buyer = getattr(main, "active_user", {})
        main.orders.append({
            "buyer": buyer,
            "product": product_name,
            "category": product.get('category', 'Unknown'),
            "quantity": qty,
            "color": color,
            "total": total
        })
        # if the stock reached 0, displays "out of stock" message
        if product_name in inv and inv[product_name]["quantity"] == 0:
            buy_btn.setEnabled(False)
            buy_btn.setText("Out of Stock")

        QMessageBox.information(
            card,
            "Order Placed",
            f"You ordered {qty} × {product_name}\n\n"
            f"Material: {product['material']}\n"
            f"Color: {color}\n"
            f"Price: {product['price']} php each\n\n"
            f"Total: {total} php"
        )

    # Connect the signal
    buy_btn.clicked.connect(buy_action)
    layout.addWidget(buy_btn)

    return card


def calculate_total(price, qty):
    if isinstance(price, (int, float)):
        return price * qty
    if isinstance(price, str) and "-" in price:
        parts = price.replace("php", "").split("-")
        try:
            low = int(parts[0].strip())
            high = int(parts[1].strip())
            return f"{low * qty} - {high * qty}"
        except ValueError:
            return price
    return price