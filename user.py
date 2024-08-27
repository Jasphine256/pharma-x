from PySide6.QtWidgets import (QMainWindow, QLabel, QGroupBox, QStackedWidget, QTreeView,
                               QToolBar, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QListView,
                               QLineEdit, QSpinBox, QDateEdit, QScrollArea, QApplication)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QPixmap, QFont, QStandardItemModel, QStandardItem
from Graph.graph import BarCanvas
from Forms.medical_form import MedicalForm
from Header.header import Header
from Tables.madical_table import DataTable
from Buttons.dash_button import DashboardButton
from Buttons.click_button import ClickButton
from Labels.view_label import ViewLabel
from Trees.medi_tree import MediTree
import pandas as pd
from database import BaseDatabase
from program_data import ProgramData
from state_manager import state_manager
import datetime
import os
import sys


class UserWindow(QMainWindow):
    meta_data = ProgramData()
    view_medicine_form = MedicalForm('edit')

    def __init__(self):

        super().__init__()

        self.setWindowTitle("JASPHINE PHARMA X V.2024.1 BY JASPHINE DIGITAL TECHNOLOGIES")
        self.setGeometry(150, 10, 1000, 700)

        self.central_widget = QStackedWidget()
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        self.toolbar = QToolBar('PHARMACIST')
        self.toolbar.setFixedWidth(300)
        self.toolbar.setMovable(False)
        self.toolbar_layout = QVBoxLayout()
        self.toolbar.setLayout(self.toolbar_layout)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.toolbar)

        self.font_big = QFont('Arial', 13)
        self.font_mid = QFont('Arial', 12)
        self.font_small = QFont('Arial', 11)
        self.font_normal = QFont('Arial', 10)
        self.font_bold = QFont('Arial', 14, QFont.Bold)
        self.font_large = QFont('Arial', 20, QFont.Bold)
        self.selected_view = ''
        self.cart = []
        self.current_price = 0
        self.grand_total = 0
        self.selected_cart_item = ()
        self.images_dir = ''
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle (e.g. PyInstaller)
            self.images_dir = os.path.join(sys._MEIPASS, 'images')
        else:
            # If the application is run from the script directly
            self.images_dir = os.path.join(os.path.abspath("."), 'images')

        self.init_ui()

    def init_ui(self):

        db = BaseDatabase('jasphine-pharma-x')

        # +++++++++++++++++++++++ FUNCTIONS ++++++++++++++++++++++++++++++++

        def show_dashboard():
            self.central_widget.setCurrentIndex(0)

        def show_add_user():
            self.central_widget.setCurrentIndex(1)

        def show_view_user():
            self.central_widget.setCurrentIndex(2)

        def show_sell_book():
            self.central_widget.setCurrentIndex(3)

        def show_profile():
            self.central_widget.setCurrentIndex(4)

        def logout():
            QApplication.exit()

        def refresh():
            self.initUI()
            self.update()
            self.repaint()

        def set_current_view(index):
            current_selection = medi_view_selector.get_model().data(index, 0)
            self.selected_view = current_selection
            current_item = medi_view_selector.get_model().itemFromIndex(index)
            parent = current_item.hasChildren()
            if not parent:
                state_manager.set_state('selected_medicine', current_selection)
                self.view_medicine_form.set_data.emit()
            else:
                pass

        def view_sale_receipt(index):
            sale_item = medicine_selector_model.itemFromIndex(index)
            selected_sale_text = medicine_selector_model.data(index, 0)
            self.selected_view = selected_sale_text
            if not sale_item.hasChildren():
                db.connect()

                data = db.fetch_row('medical', ('name', selected_sale_text))
                self.current_price = data[-1]
                data_dict = {
                    'name': data[1],
                    'description': data[2],
                    'expiry': data[4],
                    'unit': data[-1]
                }
                name.setText(data_dict['name'])
                description.setText(data_dict['description'])
                expiry_date.setText(data_dict['expiry'])
                unit_price.setText(data_dict['unit'])
                cart_btn.setEnabled(True)
            else:
                pass

        def calculate_product(value):
            num1 = self.current_price
            pdt = int(num1) * value
            unit_price.setText(str(pdt))

        def add_to_cart():
            item = []
            item_name = name.text()
            item_qty = qty_spin.value()
            item_unit = self.current_price
            item_tot = unit_price.text()
            self.grand_total += int(item_tot)
            total_btn.setText(str(self.grand_total))
            item.append(item_name)
            item.append(item_qty)
            item.append(item_unit)
            item.append(item_tot)
            self.cart.append(item)
            model_item = QStandardItem(f"{item_name}: {item_qty} @{item_unit} -->{item_tot}")
            cart_list_model.appendRow(model_item)
            action_btns.setEnabled(True)
            cart_btn.setEnabled(False)

        def clear_cart():
            cart_list_model.clear()
            self.grand_total = 0
            self.cart = []
            total_btn.setText('00000')
            action_btns.setEnabled(False)

        def remove_cart_item():
            if cart_list_model.rowCount() != 0:
                if self.selected_cart_item:
                    index = self.selected_cart_item[1]
                    item = cart_list_model.itemFromIndex(index).row()
                    cart_list_model.removeRow(item)
                    price_deduction = 0
                    cart_index = 0

                    for i in self.cart:
                        n = self.selected_cart_item[0].index(':')
                        if self.selected_cart_item[0][:n] in i:
                            price_deduction = int(i[-1])
                            cart_index = self.cart.index(i)
                    self.grand_total -= price_deduction
                    total_btn.setText(str(self.grand_total))
                    self.cart.pop(cart_index)
            else:
                pass

        def set_current_cart_item(index):
            selected = cart_list_model.data(index, 0)
            self.selected_cart_item = (selected, index)

        def complete_purchase():
            if self.cart:
                for i in self.cart:
                    name = i[0]
                    qty = i[1]
                    unit = i[2]
                    tot = i[3]
                    data_dict = {
                        'name': name,
                        'quantity': qty,
                        'price': unit,
                        'total': tot
                    }
                    db.connect()
                    if db.table_exists('sales'):
                        db.insert_data('sales', data_dict)
                        db.commit_changes()
                        self.cart = []
                        self.selected_cart_item = ()
                        self.grand_total = 0
                        cart_list_model.clear()
                        total_btn.setText('00000')
                        action_btns.setEnabled(False)
                    else:
                        columns_dict = {
                            'id': "INTEGER PRIMARY KEY AUTOINCREMENT",
                            'name': "TEXT NOT NULL",
                            'quantity': "TEXT NOT NULL",
                            'price': "TEXT NOT NULL",
                            'total': "TEXT NOT NULL",
                        }
                        db.create_table('sales', columns_dict)
                        db.insert_data('sales', data_dict)
                        db.commit_changes()
                    db.close_connection()
                    self.cart = []
                    self.selected_cart_item = ()
                    self.grand_total = 0
                    cart_list_model.clear()
                    total_btn.setText('00000')
                    action_btns.setEnabled(False)
            else:
                pass

        # ++++++++++++++++++++++++ TOOLBAR CONTENT ++++++++++++++++++++++++++

        health_pixmap = QPixmap(os.path.join(self.images_dir, 'health.png')).scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
        image_label = ViewLabel(pixmap=health_pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.toolbar.addWidget(image_label)

        admin_name = ViewLabel(text=state_manager.get_states('username'), font=self.font_large)
        admin_name.setFixedHeight(60)
        admin_name.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.toolbar.addWidget(admin_name)

        admin_label = ViewLabel(text="PHARMACIST", font=self.font_big)
        admin_label.setFixedHeight(60)
        admin_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.toolbar.addWidget(admin_label)

        button_group = QGroupBox()
        button_group.setProperty('class', 'dash-btn-group')
        button_group.setMinimumHeight(340)
        buttons_layout = QVBoxLayout(button_group)
        self.toolbar.addWidget(button_group)

        dashboard_button = DashboardButton("   Dashboard  ", show_dashboard, 'dashboard.png')
        buttons_layout.addWidget(dashboard_button)

        add_button = DashboardButton("   Add medicine", show_add_user, 'add.png')
        buttons_layout.addWidget(add_button)

        view_button = DashboardButton("  View medicine", show_view_user, 'view.png')
        buttons_layout.addWidget(view_button)

        sell_button = DashboardButton("   Sell medicine", show_sell_book, 'view.png')
        buttons_layout.addWidget(sell_button)

        about_button = DashboardButton("   About             ", show_profile, "about.png")
        buttons_layout.addWidget(about_button)

        logout_button = DashboardButton("   Logout           ", logout, 'logout.png')
        logout_button.setProperty('class', 'logout-btn')
        buttons_layout.addWidget(logout_button)

        # +++++++++++++++++++++++++ DASHBOARD CONTENT +++++++++++++++++++++++++++

        dashboard = QWidget()
        dashboard_layout = QVBoxLayout(dashboard)
        self.central_widget.addWidget(dashboard)

        header = QWidget()
        header_layout = QHBoxLayout(header)
        header.setFixedHeight(50)
        dashboard_layout.addWidget(header)

        header_label = ViewLabel(text="Dashboard", font=self.font_large)
        header_layout.addWidget(header_label)

        refresh_btn = ClickButton('refresh', refresh)
        refresh_btn.setFixedWidth(100)
        header_layout.addWidget(refresh_btn)

        graph = BarCanvas()
        db.connect()
        valid_medicine = []
        expired_medicine = []
        if db.table_exists('medical'):
            medicines = db.fetch_column('medical', 'name, expiry')
            for medicine in medicines:
                exp_date = medicine[1]
                now_date = datetime.datetime.now().strftime('%d/%m/%Y')
                formated_now = datetime.datetime.strptime(now_date, '%d/%m/%Y')
                formated_exp = datetime.datetime.strptime(exp_date, '%d/%m/%Y')
                if formated_exp > formated_now:
                    valid_medicine.append(medicine[0])
                else:
                    expired_medicine.append(medicine[0])
            graph.plot(data=[len(valid_medicine), len(expired_medicine)], labels=['Valid', 'Expired'])
            dashboard_layout.addWidget(graph)
        else:
            graph.plot(data=[0, 0], labels=['Valid', 'Expired'])
            dashboard_layout.addWidget(graph)

        if db.table_exists('sales'):
            table_data = pd.DataFrame(db.fetch_all_data('sales'))
            medi_table = DataTable(table_data)
            dashboard_layout.addWidget(medi_table)
        else:
            medi_table = DataTable(pd.DataFrame(['no sales']))
            dashboard_layout.addWidget(medi_table)
        db.close_connection()

        #  ++++++++++++++++++++++++++++ ADD MEDICINE PAGE ++++++++++++++++++++++++

        users_page = QWidget()
        users_page_layout = QVBoxLayout(users_page)
        self.central_widget.addWidget(users_page)

        users_header = Header('Add New Medicine')
        users_page_layout.addWidget(users_header)

        add_medicine_form = MedicalForm('create')
        users_page_layout.addWidget(add_medicine_form)

        #  ++++++++++++++++++++++++++++ VIEW MEDICINE PAGE ++++++++++++++++++++++++

        viewer_page = QWidget()
        viewer_page_layout = QVBoxLayout(viewer_page)
        self.central_widget.addWidget(viewer_page)

        viewer_header = Header('View medicine')
        viewer_page_layout.addWidget(viewer_header)

        user_view = QWidget()
        user_view_layout = QHBoxLayout(user_view)
        viewer_page_layout.addWidget(user_view)

        medi_view_selector = MediTree(set_current_view)
        user_view_layout.addWidget(medi_view_selector)

        user_view_layout.addWidget(self.view_medicine_form)

        #  ++++++++++++++++++++++++++++ SELL MEDICINE PAGE ++++++++++++++++++++++++

        sell_page = QWidget()
        sell_page_layout = QVBoxLayout()
        sell_page.setLayout(sell_page_layout)
        self.central_widget.addWidget(sell_page)

        sell_header = Header('Sell medicine')
        sell_page_layout.addWidget(sell_header)

        sell_book = QGroupBox()
        sell_book.setMinimumHeight(500)
        sell_book_layout = QHBoxLayout()
        sell_book.setLayout(sell_book_layout)
        sell_page_layout.addWidget(sell_book)

        medicine_selector = QTreeView()
        medicine_selector.clicked.connect(view_sale_receipt)
        medicine_selector.setMaximumWidth(180)
        medicine_selector.setMinimumHeight(500)
        medicine_selector_model = QStandardItemModel()
        medicine_selector.setModel(medicine_selector_model)
        medicine_selector_model.setHorizontalHeaderLabels(['Medicine Explorer'])
        sell_book_layout.addWidget(medicine_selector)

        valid_medicine_tree = QStandardItem('Valid medicine')
        valid_medicine_tree.setFont(self.font_normal)
        medicine_selector_model.appendRow(valid_medicine_tree)
        db.connect()
        valid_tree_medicine = []
        if db.table_exists('medical'):
            valid_medicines = db.fetch_column('medical', 'name, expiry')
            for medicine in valid_medicines:
                exp_date = medicine[1]
                now_date = datetime.datetime.now().strftime('%d/%m/%Y')
                formated_now = datetime.datetime.strptime(now_date, '%d/%m/%Y')
                formated_exp = datetime.datetime.strptime(exp_date, '%d/%m/%Y')
                if formated_exp > formated_now:
                    valid_tree_medicine.append(medicine[0])
                else:
                    pass

        db.close_connection()

        if valid_tree_medicine:
            for valid in valid_tree_medicine:
                option = QStandardItem(valid)
                valid_medicine_tree.appendRow(option)
        else:
            no3 = QStandardItem('no medicine')
            no3.setEnabled(False)
            valid_medicine_tree.appendRow(no3)

        sell_form = QWidget()
        sell_form.setMaximumWidth(500)
        sell_form_layout = QVBoxLayout()
        sell_form.setLayout(sell_form_layout)
        sell_book_layout.addWidget(sell_form)

        form = QGroupBox()
        form.setFixedWidth(300)
        form.setFixedHeight(400)
        form_layout = QVBoxLayout()
        form.setLayout(form_layout)
        name = QPushButton('')
        name.setFont(self.font_big)
        name.setMaximumHeight(80)
        name.setEnabled(False)
        form_layout.addWidget(name)
        description = QPushButton('')
        description.setFont(self.font_small)
        description.setMaximumHeight(80)
        description.setEnabled(False)
        form_layout.addWidget(description)
        expiry_date = QPushButton('')
        expiry_date.setFont(self.font_big)
        expiry_date.setEnabled(False)
        expiry_date.setMaximumHeight(80)
        form_layout.addWidget(expiry_date)
        unit_price = QPushButton('000000')
        unit_price.setEnabled(False)
        unit_price.setFont(self.font_bold)
        unit_price.setMaximumHeight(80)
        qty_box = QWidget()
        form_layout.addWidget(qty_box)
        qty_box_layout = QHBoxLayout()
        qty_box.setLayout(qty_box_layout)
        qty_label = QLabel("Enter Quantity ")
        qty_spin = QSpinBox()
        qty_spin.setRange(1, 10000)
        qty_spin.setValue(1)
        qty_spin.valueChanged.connect(calculate_product)
        qty_box_layout.addWidget(qty_label)
        qty_box_layout.addWidget(qty_spin)
        form_layout.addWidget(unit_price)

        cart_btn = ClickButton('Add To Cart', add_to_cart)
        if self.selected_view == '':
            cart_btn.setEnabled(False)
        form_layout.addWidget(cart_btn)

        sell_form_layout.addWidget(form)

        sell_cart = QWidget()
        sell_cart_layout = QVBoxLayout()
        sell_cart.setLayout(sell_cart_layout)
        sell_book_layout.addWidget(sell_cart)

        cart_list = QListView()
        cart_list.clicked.connect(set_current_cart_item)
        cart_list_model = QStandardItemModel()
        cart_list.setModel(cart_list_model)
        sell_cart_layout.addWidget(cart_list)

        action_btns = QWidget()
        action_btns_layout = QHBoxLayout()
        action_btns.setLayout(action_btns_layout)
        sell_cart_layout.addWidget(action_btns)

        total_btn = QPushButton('00000')
        total_btn.setEnabled(False)
        total_btn.setFixedHeight(60)
        total_btn.setFont(self.font_big)
        action_btns_layout.addWidget(total_btn)

        delete_btn = ClickButton('Remove', remove_cart_item)

        action_btns_layout.addWidget(delete_btn)

        clear_btn = ClickButton('Clear', clear_cart)
        action_btns_layout.addWidget(clear_btn)

        purchase_btn = ClickButton('Purchase', complete_purchase)
        action_btns_layout.addWidget(purchase_btn)
        if not self.cart:
            action_btns.setEnabled(False)

        #  ++++++++++++++++++++++++++++ ABOUT USER PAGE ++++++++++++++++++++++++

        profile_page = QWidget()
        profile_page_layout = QVBoxLayout()
        profile_page.setLayout(profile_page_layout)

        self.central_widget.addWidget(profile_page)

        profile_header = Header('About The Developer')
        profile_page_layout.addWidget(profile_header)

        dev_info = QGroupBox()
        dev_info.setMaximumHeight(500)
        dev_info_layout = QVBoxLayout()
        dev_info.setLayout(dev_info_layout)
        header_text = QLabel(self.meta_data.software_name())
        header_text.setFont(self.font_bold)
        dev_info_layout.addWidget(header_text)

        header_sub_text = QLabel(f"By {self.meta_data.software_developer()}")
        header_sub_text.setFont(self.font_big)
        dev_info_layout.addWidget(header_sub_text)

        header_sub_text2 = QLabel(self.meta_data.developer_contact())
        header_sub_text2.setFont(self.font_mid)
        dev_info_layout.addWidget(header_sub_text2)

        about_scroller = QScrollArea()
        about_scroller.setWidgetResizable(True)
        info_text = QLabel(self.meta_data.license_data())
        info_text.setAlignment(Qt.AlignmentFlag.AlignTop)
        info_text.setFont(self.font_normal)
        about_scroller.setWidget(info_text)

        dev_info_layout.addWidget(about_scroller)
        profile_page_layout.addWidget(dev_info)
