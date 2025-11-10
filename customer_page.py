from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QLineEdit,
    QGroupBox, QHBoxLayout, QSpinBox, QMessageBox, QComboBox, QCheckBox, QGridLayout, QTableWidget, QTableWidgetItem, 
    QHeaderView, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QColor
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

    header_layout = QGridLayout()
    title = QLabel("👜 Product Catalog")
    title.setStyleSheet("font-size: 30px; font-weight: bold; color: #222;")
    title.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    title.setContentsMargins(0, 0, 0, 0)

    shadow_effect = QGraphicsDropShadowEffect()
    shadow_effect.setBlurRadius(30)
    shadow_effect.setColor(QColor(50,50,50,180))
    shadow_effect.setOffset(4, 4)
    title.setGraphicsEffect(shadow_effect)

    # Create menu panel for user options
    from ui_components import CollapsablePanel
    from feedback_email import send_feedback_email
    menu_panel = CollapsablePanel(widget)
    
    def show_feedback():
        from ui_views import FeedbackDialog
        dialog = FeedbackDialog(widget)
        dialog.exec()
    
    menu_panel.add_menu_item("Send Feedback", show_feedback)
    menu_panel.add_menu_item("Log Out", lambda: parent.switch_view('customer'))

    menu_btn = QPushButton("☰")
    menu_btn.setFixedSize(30, 30)
    menu_btn.setStyleSheet("""
        QPushButton {
            background: transparent;
            border: none;
            font-size: 20px;
            color: #222222;
        }
        QPushButton:hover {
            color: #666666;
        }
    """)
    menu_btn.clicked.connect(menu_panel.toggle)
    
    # Place the title in the central column and center it, with menu button on the left
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    header_layout.setColumnStretch(0, 1)
    header_layout.setColumnStretch(1, 0)
    header_layout.setColumnStretch(2, 1)
    header_layout.addWidget(menu_btn, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
    header_layout.addWidget(title, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)

    cart_button = QPushButton()
    cart_button.setFlat(True)
    cart_button.setFixedSize(100, 100)
    cart_button.setStyleSheet("""
        QPushButton {
            border: none;
        }
    """)
    cart_layout = QHBoxLayout(cart_button)
    cart_layout.setSpacing(5)
    cart_icon_label = QLabel("🛒")
    cart_icon_label.setStyleSheet("font-size: 30px;")
    cart_count_label = QLabel("(0)")
    cart_count_label.setStyleSheet("font-size: 25px; font-weight: bold;")
    parent.cart_count_label = cart_count_label
    cart_layout.addWidget(cart_icon_label)
    cart_layout.addWidget(cart_count_label)
    header_layout.addWidget(cart_button, 0, 2, alignment=Qt.AlignmentFlag.AlignRight)
    layout.addLayout(header_layout)

    desc = QLabel("Select color and quantity for each item, then click Buy to order.")
    desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
    desc.setStyleSheet("color: #555; font-size: 14px; margin-bottom: 10px;")
    layout.addWidget(desc)

    #filter control
    top_filter_layout = QHBoxLayout()

    search_bar = QLineEdit()
    search_bar.setPlaceholderText("Search by product name...")
    search_bar.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 5px;")
    top_filter_layout.addWidget(search_bar)

    clear_filters_btn = QPushButton("Clear Filters")
    clear_filters_btn.setStyleSheet("""
        QPushButton {
            background: #6c757d; color: white; border: none;
            padding: 6px 12px; border-radius: 5px;
        }
        QPushButton:hover { background: #5a6268; }
    """)
    top_filter_layout.addWidget(clear_filters_btn)

    layout.addLayout(top_filter_layout)

    # Checkbox filters container
    filter_container = QWidget()
    filter_grid = QGridLayout(filter_container)
    filter_grid.setContentsMargins(0, 10, 0, 10)
    filter_grid.setSpacing(10)

    category_group_box = QGroupBox("Filter by Category")
    category_layout = QHBoxLayout(category_group_box)
    filter_grid.addWidget(category_group_box, 0, 0)

    material_group_box = QGroupBox("Filter by Material")
    material_layout = QHBoxLayout(material_group_box)
    filter_grid.addWidget(material_group_box, 0, 1)

    layout.addWidget(filter_container)

    # Scroll area
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    content = QWidget()
    content_layout = QVBoxLayout(content)
    content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    content_layout.setSpacing(20)

    # "No results" message
    no_results_label = QLabel("No products match your search.")
    no_results_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    no_results_label.setStyleSheet("font-size: 16px; color: #888; margin-top: 50px;")
    content_layout.addWidget(no_results_label)
    no_results_label.hide()  # Hide it initially

    # Product Catalog
    catalog = {
        "Shoulder Bag": [
            {"price": 300, "material": "Crocodile Texture", "name": "CARA", "colors": ["Blue/Pink", "Red/Blue", "Pink/Brown", "Brown/Pink", "Pink/Blue", "Tan/Beige", "Beige/Black", "Blue/Tan", "Black/Red", "Brown/Beige"]},
            {"price": 350, "material": "Faux Leather", "name": "ANA", "colors": ["Brown", "Taupe", "Lt. Green", "Dark Brown"]},
            {"price": 350, "material": "Faux Leather", "name": "HYE", "colors": ["Gray", "Choco Brown", "Black"]},
            {"price": 300, "material": "Faux Leather", "name": "BABY", "colors": ["Brown"]},
            {"price": 280, "material": "Faux Leather", "name": "BIA", "colors": ["Lt. Green"]},
        ],
        "Sling Bag": [
            {"price": 1000, "material": "Real Leather", "name": "NYA", "colors": ["Tan", "Black"]},
            {"price": 680, "material": "Leather", "name": "ORA", "colors": ["Tan", "Black"]},
        ],
        "Tote Bag": [
            {"price": 1200, "material": "Real Leather", "name": "QUI", "colors": ["Black"]},
            {"price": 1800, "material": "Real Leather", "name": "LIA", "colors": ["Brown", "Black", "Tan"]},
        ],
        "Coin Purse": [
            {"price": 70, "material": "Faux Leather", "name": "MEG", "colors": ["Brown", "Mocca", "Red", "Tan", "R. Blue", "D. Brown"]},
            {"price": 70, "material": "Faux Leather", "name": "AURA", "colors": ["Tan", "Brown G", "Camel", "Taupe", "Red", "Black", "Brown", "Gray"]},
            {"price": 50, "material": "Faux Leather", "name": "EVA", "colors": ["Blue", "Tan", "Old Rose", "Mocca", "Gray", "Red", "Taupe", "Brown", "Camel", "Black"]},
            {"price": 50, "material": "Faux Leather", "name": "AVA", "colors": ["Brown", "Tan", "Red", "Black", "Old Rose", "Mocca", "Taupe", "Beige", "Gray", "Blue", "Lt. Green"]},
        ],
        "Saddle Bag": [
            {"price": "1800", "material": "Faux Leather", "name": "STANDARD", "colors": ["Standard"]},
            {"price": "5500 - 6000", "material": "Leather", "name": "CUSTOMIZED", "colors": ["Customizable"]},
        ],
    }

    product_widgets = []
    all_materials = set()
    
    category_checkboxes = []
    material_checkboxes = []

    for category, items in catalog.items():
        # --- Category Section Widget ---
        category_section_widget = QWidget()
        category_section_layout = QVBoxLayout(category_section_widget)
        category_section_layout.setContentsMargins(0, 0, 0, 0)
        category_section_layout.setSpacing(5)

        section_label = QLabel(f"{category}")
        section_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #222; margin-top: 10px;")
        category_section_layout.addWidget(section_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # --- Horizontal Scroll Area for Products ---
        h_scroll = QScrollArea()
        h_scroll.setWidgetResizable(True)
        h_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        h_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        h_scroll.setFixedHeight(300) # Adjust height to fit cards + shadow

        scroll_content = QWidget()
        h_layout = QHBoxLayout(scroll_content)
        h_layout.setSpacing(15)
        
        for item in items:
            all_materials.add(item["material"])
            card = create_product_card(item, category, parent) 
            h_layout.addWidget(card)
            parent.product_card_map[item['name']] = card

        h_scroll.setWidget(scroll_content)
        category_section_layout.addWidget(h_scroll)
        content_layout.addWidget(category_section_widget)
        product_widgets.append({'widget': category_section_widget, 'type': 'section', 'category': category, 'data': items})

    # Initial update of cart count
    parent.update_cart_count()

    for category_name in catalog.keys():
        cb = QCheckBox(category_name)
        cb.setStyleSheet("""
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
                border: 1px solid #888;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background-color: #222222;
                border: 1px solid #222222;
            }
        """)
        category_layout.addWidget(cb)
        category_checkboxes.append(cb)

    # Populate material checkboxes
    for material_name in sorted(list(all_materials)):
        cb = QCheckBox(material_name)
        cb.setStyleSheet("""
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
                border: 1px solid #888;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background-color: #222222;
                border: 1px solid #222222;
            }
        """)
        material_layout.addWidget(cb)
        material_checkboxes.append(cb)

    content_layout.addStretch(1)
    scroll.setWidget(content)
    layout.addWidget(scroll)

    def update_product_view():
        search_text = search_bar.text().lower()
        
        checked_categories = {cb.text() for cb in category_checkboxes if cb.isChecked()}
        checked_materials = {cb.text() for cb in material_checkboxes if cb.isChecked()}

        visible_product_categories = set()

        for item in product_widgets:
            is_visible = False
            category_name = (item.get('category') or '').lower()

            category_filter_ok = not checked_categories or item['category'] in checked_categories
            if not category_filter_ok:
                item['widget'].hide()
                continue

            if search_text and search_text in category_name:
                is_visible = True
                visible_product_categories.add(item['category'])
            else:

                for product_data in item['data']:
                    name_match = search_text in product_data['name'].lower() if search_text else True
                    material_match = not checked_materials or product_data['material'] in checked_materials
                    if name_match and material_match:
                        is_visible = True
                        visible_product_categories.add(item['category'])
                        break

            if is_visible:
                item['widget'].show()
            else:
                item['widget'].hide()

        if not visible_product_categories:
            no_results_label.show()
        else:
            no_results_label.hide()

    search_bar.textChanged.connect(update_product_view)
    
    for cb in category_checkboxes:
        cb.stateChanged.connect(update_product_view)
    
    for cb in material_checkboxes:
        cb.stateChanged.connect(update_product_view)
    
    def clear_checkbox_filters():

        for cb in category_checkboxes + material_checkboxes:
            cb.blockSignals(True)

        for cb in category_checkboxes + material_checkboxes:
            cb.setChecked(False)

        for cb in category_checkboxes + material_checkboxes:
            cb.blockSignals(False)
        update_product_view()
    clear_filters_btn.clicked.connect(clear_checkbox_filters)

    cart_button.clicked.connect(lambda: parent.switch_view('shopping_cart'))

    return widget


def create_product_card(product, category, main_window):

    card = QGroupBox()
    card.product_name = product['name']
    card.product_material = product['material']
    card.setFixedWidth(220)
    card.setStyleSheet("""
        QGroupBox {
            border: 1px solid #e0e0e0; border-radius: 8px;
            background: #fafafa;
        }
        QGroupBox:hover {
            border-color: #0078d7;
        }
    """)

    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(15)
    shadow.setXOffset(0)
    shadow.setYOffset(2)
    shadow.setColor(Qt.GlobalColor.gray)
    card.setGraphicsEffect(shadow)

    card_layout = QVBoxLayout(card)
    card_layout.setContentsMargins(10, 10, 10, 10)
    card_layout.setSpacing(10)
    card_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    # Images
    image_label = QLabel()
    image_label.setFixedSize(100, 100)
    image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.abspath(__file__))

    def find_image(name):
        variants = [name, name.lower(), name.upper(), name.title()]
        exts = ['.jpg', '.png', '.jpeg']
        for v in variants:
            for e in exts:
                p = os.path.join(base_dir, 'assets', f"{v}{e}")
                if os.path.exists(p):
                    return p
        return None

    image_path = find_image(product['name'])
    pixmap = QPixmap(image_path) if image_path else QPixmap()

    if not pixmap.isNull():
        image_label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
    else:
        # helpful debug code for errors
        print(f"[WARN] Image not found for product '{product['name']}' — looked for variants and extensions in assets/")
        image_label.setText("Image\nNot Found")
        image_label.setStyleSheet("""
        QLabel {
            background-color: #e0e0e0;
            border: 1px dashed #cccccc;
            border-radius: 5px;
            color: #888888;
        }
        """)

    card_layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter)

    inv = main_window.inventory_data
    stock_text = ""
    # look up stock
    if product["name"] in inv and "Customized" not in product["name"]:
        stock_left = inv[product["name"]]["quantity"]
        stock_text = f"  —  {stock_left} left"
        if stock_left == 0:
            stock_text = "  —  Out of Stock"
    else:
        stock_text = "  —  Customizable"
    card.name_label = QLabel(f"{product['material']}: {product['name']}{stock_text}")
    card.name_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
    card.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    card.name_label.setWordWrap(True)
    card_layout.addWidget(card.name_label)

    price_label = QLabel(f"{product['price']} php")
    price_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #222;")
    price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    card_layout.addWidget(price_label)

    # QOL
    controls_layout = QHBoxLayout()
    controls_layout.setSpacing(10)

    color_box = QComboBox()
    color_box.addItems(product["colors"])
    controls_layout.addWidget(color_box)

    qty_spin = QSpinBox()
    qty_spin.setRange(1, 99)
    qty_spin.setValue(1)
    qty_spin.setFixedWidth(60)
    controls_layout.addWidget(qty_spin)
    card_layout.addLayout(controls_layout)

    card_layout.addStretch(1)

    card.buy_btn = QPushButton("Add to Cart")
    card.buy_btn.setStyleSheet("""
        QPushButton {
            background: #28a745; color: white;
            border: none; padding: 6px 12px; border-radius: 5px;
        }
        QPushButton:hover { background: #218838; }
    """)
    card_layout.addWidget(card.buy_btn)

    def buy_action():
        qty = qty_spin.value()
        color = color_box.currentText()
        total = calculate_total(product['price'], qty)
        
        inv = getattr(main_window, "inventory_data", {})
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
            inv[product_name]["quantity"] -= qty
            # Update the product card's display immediately
            main_window.update_product_card_display(product_name)

        # Record order (add to cart)
        main_window.cart_items.append({ # type: ignore
            "buyer": main_window.active_user,
            "product": product_name,
            "category": category,
            "quantity": qty,
            "color": color,
            "price": product['price'],
            "total": total
        })

        # Update the cart count display
        main_window.update_cart_count()

        QMessageBox.information(
            card,
            "Added to Cart",
            f"You added {qty} × {product_name} to your cart.\n\n"
            f"Material: {product['material']}\n"
            f"Color: {color}\n"
            f"Price: {product['price']} php each\n\n"
            f"Total: {total} php"
        )

    # Connect the signal
    card.buy_btn.clicked.connect(buy_action)

    # Initial check for out of stock to disable button
    if product["name"] in inv and "Customized" not in product["name"] and inv[product["name"]]["quantity"] == 0:
        card.buy_btn.setEnabled(False)
        card.buy_btn.setText("Out of Stock")

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

def create_cart_view(parent=None):
    widget = QWidget(parent)
    layout = QVBoxLayout(widget)
    layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    layout.setContentsMargins(40, 20, 40, 20)
    layout.setSpacing(15)

    title = QLabel("🛒 Your Shopping Cart")
    title.setStyleSheet("font-size: 30px; font-weight: bold; color: #222;")
    layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

    # Table for cart items
    cart_table = QTableWidget()
    cart_table.setColumnCount(6)
    cart_table.setHorizontalHeaderLabels(["Product", "Color", "Quantity", "Unit Price", "Subtotal", "Actions"])
    header = cart_table.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    cart_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    layout.addWidget(cart_table)

    # Total price label
    total_price_label = QLabel("Total: 0 php")
    total_price_label.setAlignment(Qt.AlignmentFlag.AlignRight)
    total_price_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")
    layout.addWidget(total_price_label)

    def refresh_cart_table():
        cart_table.setRowCount(0) # Clear the table
        cart_items = getattr(parent, 'cart_items', [])
        cart_table.setRowCount(len(cart_items))
        grand_total = 0

        for row, item in enumerate(cart_items):
            subtotal = item.get('total', 0)
            if isinstance(subtotal, (int, float)):
                grand_total += subtotal

            cart_table.setItem(row, 0, QTableWidgetItem(item.get('product', '')))
            cart_table.setItem(row, 1, QTableWidgetItem(item.get('color', '')))
            cart_table.setItem(row, 2, QTableWidgetItem(str(item.get('quantity', ''))))
            cart_table.setItem(row, 3, QTableWidgetItem(str(item.get('price', ''))))
            cart_table.setItem(row, 4, QTableWidgetItem(str(subtotal)))

            remove_btn = QPushButton("Remove")
            remove_btn.setStyleSheet("""
                QPushButton { background-color: #dc3545; color: white; border-radius: 4px; padding: 4px 8px; }
                QPushButton:hover { background-color: #c82333; }
            """)
            remove_btn.clicked.connect(create_remove_handler(item))
            cart_table.setCellWidget(row, 5, remove_btn)

        total_price_label.setText(f"Total: {grand_total} php")

    def create_remove_handler(item_to_remove):
        def handler():
            product_name_for_msg = item_to_remove.get('product', 'this item')
            reply = QMessageBox.question(
                widget,
                'Confirm Removal',
                f"Are you sure you want to remove {product_name_for_msg} from your cart?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                # Restore stock (only for trackable items)
                inv = getattr(parent, "inventory_data", {})
                product_name = item_to_remove.get('product')
                if product_name in inv and "Customized" not in product_name:
                    inv[product_name]["quantity"] += item_to_remove.get('quantity', 0)

                # Remove from cart
                parent.cart_items.remove(item_to_remove)
                
                refresh_cart_table()

        return handler

    # Populate Table
    refresh_cart_table()

    #Action Buttons
    button_layout = QHBoxLayout()
    button_layout.addStretch()

    back_btn = QPushButton("Back to Catalog")
    back_btn.setStyleSheet("""
        QPushButton {
            background: #6c757d; color: white; border: none;
            padding: 8px 16px; border-radius: 5px; font-size: 14px;
        }
        QPushButton:hover { background: #5a6268; }
    """)
    button_layout.addWidget(back_btn)

    checkout_btn = QPushButton("Checkout")
    checkout_btn.setStyleSheet("""
        QPushButton {
            background: #28a745; color: white; border: none;
            padding: 8px 16px; border-radius: 5px; font-size: 14px;
        }
        QPushButton:hover { background: #218838; }
    """)
    button_layout.addWidget(checkout_btn)
    layout.addLayout(button_layout)

    def handle_checkout():
        if not parent.cart_items:
            QMessageBox.information(widget, "Empty Cart", "Your cart is empty.")
            return

        # Move items from cart to final orders
        parent.orders.extend(parent.cart_items)
        # Clear the cart
        parent.cart_items.clear()

        QMessageBox.information(
            widget,
            "Order Placed!",
            "Thank you for your order! Your items are now being processed."
        )
        # Go back to the catalog, which will now show an empty cart
        parent.switch_view('customer_catalog')

    back_btn.clicked.connect(lambda: parent.switch_view('customer_catalog'))
    checkout_btn.clicked.connect(handle_checkout)

    # If cart is empty, disable checkout
    if not getattr(parent, 'cart_items', []):
        checkout_btn.setEnabled(False)
        checkout_btn.setStyleSheet("background-color: #ccc; color: #666; border: none; padding: 8px 16px; border-radius: 5px; font-size: 14px;")

    return widget