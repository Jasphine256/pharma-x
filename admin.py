from PySide6.QtWidgets import (QMainWindow, QLabel, QGroupBox, QStackedWidget, QTreeView,
                               QToolBar, QPushButton, QVBoxLayout, QWidget, QHBoxLayout,
                               QScrollArea, QApplication)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont, QStandardItemModel, QStandardItem
from Cards.card import Card
from Footer.footer import Footer
from Forms.user_form import UserForm
from Header.header import Header
from Buttons.dash_button import DashboardButton
from state_manager import state_manager
from PySide6.QtCore import Signal
from database import BaseDatabase
from program_data import ProgramData
import sys
import os


class AdminWindow(QMainWindow):
    current_update = []
    tree_updater_signal = Signal()
    meta_data = ProgramData()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("JASPHINE PHARMA X V.2024.1 BY JASPHINE DIGITAL TECHNOLOGIES")
        self.setGeometry(150, 10, 1000, 700)

        self.central_widget = QStackedWidget()
        self.main_layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        self.toolbar = QToolBar('ADMINISTRATOR')
        self.toolbar.setFixedWidth(300)
        self.toolbar.setMovable(False)
        self.toolbar_layout = QVBoxLayout(self.toolbar)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.toolbar)

        self.font_big = QFont('Arial', 13)
        self.font_mid = QFont('Arial', 12)
        self.font_small = QFont('Arial', 11)
        self.font_normal = QFont('Arial', 10)
        self.font_bold = QFont('Arial', 14, QFont.Bold)
        self.font_large = QFont('Arial', 20, QFont.Bold)

        self.images_dir = ''

        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle (e.g. PyInstaller)
            self.images_dir = os.path.join(sys._MEIPASS, 'images')
        else:
            # If the application is run from the script directly
            self.images_dir = os.path.join(os.path.abspath("."), 'images')

        self.current_view_data = {'role': '', 'name': '', 'username': '',
                                  'dob': '', 'contact': '', 'email': '', 'password': ''}

        self.user_view_form = UserForm('edit', self.current_view_data)

        self.init_ui()

    def init_ui(self):
        db = BaseDatabase('jasphine-pharma-x')

        # ++++++++++++++++++++++++++++++ FUNCTIONS ++++++++++++++++++++++++++++

        def view_profile(index):
            parent = user_selector_model.hasChildren(index)
            if not parent:
                current_profile = user_selector_model.data(index, role=0)
                state_manager.set_state('selected_user', current_profile)
                self.user_view_form.set_data.emit(current_profile)
            else:
                pass

        def update_user_tree():
            self.tree_updater_signal.emit()

        def refetch_tree_data():
            admin_tree.removeRows(0, admin_tree.rowCount())
            db.connect()
            if db.table_exists('users'):
                new_data = db.fetch_columns('users', 'username', ('role', 'Administrator',))
                for user_name in new_data:
                    option = QStandardItem(user_name[0])
                    admin_tree.appendRow(option)
            else:
                option_no = QStandardItem('No Admins')
                option_no.setEnabled(False)
                admin_tree.appendRow(option_no)

            user_tree.removeRows(0, user_tree.rowCount())
            if db.table_exists('users'):
                new_data = db.fetch_columns('users', 'username', ('role', 'Pharmacist',))
                for user_name in new_data:
                    option = QStandardItem(user_name[0])
                    user_tree.appendRow(option)
            else:
                option_no = QStandardItem('No Pharmacists')
                option_no.setEnabled(False)
                user_tree.appendRow(option_no)

        def show_dashboard():
            self.central_widget.setCurrentIndex(0)

        def show_add_user():
            self.central_widget.setCurrentIndex(1)

        def show_view_user():
            self.central_widget.setCurrentIndex(2)

        def show_profile():
            self.central_widget.setCurrentIndex(3)

        def logout():
            QApplication.exit()

        # ++++++++++++++++++++++++ TOOLBAR CONTENT ++++++++++++++++++++++++++

        pixmap = QPixmap(os.path.join(self.images_dir, 'admin-icon.png')).scaled(
            200, 200,
            Qt.AspectRatioMode.KeepAspectRatio)

        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.toolbar.addWidget(image_label)

        admin_name = QLabel(state_manager.get_states('username'))
        admin_name.setFont(self.font_large)
        admin_name.setFixedHeight(60)
        admin_name.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.toolbar.addWidget(admin_name)

        admin_label = QLabel("ADMINISTRATOR")
        admin_label.setFont(self.font_big)
        admin_label.setFixedHeight(60)
        admin_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.toolbar.addWidget(admin_label)

        button_group = QGroupBox()
        button_group.setProperty('class', 'dash-btn-group')
        buttons_layout = QVBoxLayout(button_group)
        self.toolbar.addWidget(button_group)

        # TOOLBAR NAVIGATION BUTTONS

        dashboard_button = DashboardButton("   Dashboard", show_dashboard, 'dashboard.png')
        buttons_layout.addWidget(dashboard_button)

        add_button = DashboardButton("   Add User   ", show_add_user, 'add.png')
        buttons_layout.addWidget(add_button)

        view_button = DashboardButton("  View Users  ", show_view_user, 'view.png')
        buttons_layout.addWidget(view_button)

        about_button = DashboardButton("   About         ", show_profile, 'about.png')
        buttons_layout.addWidget(about_button)

        logout_button = DashboardButton("   Logout       ", logout, 'logout.png')
        logout_button.setProperty('class', 'logout-btn')
        buttons_layout.addWidget(logout_button)

        # +++++++++++++++++++++++++ DASHBOARD CONTENT +++++++++++++++++++++++++++

        dashboard = QWidget()
        dashboard_layout = QVBoxLayout(dashboard)
        self.central_widget.addWidget(dashboard)

        header_label = Header('Dashboard')
        dashboard_layout.addWidget(header_label)

        footer = Footer()
        dashboard_layout.addWidget(footer)

        feature_view = QWidget()
        feature_view_layout = QHBoxLayout(feature_view)
        dashboard_layout.addWidget(feature_view)

        admin_info_group = Card(title='ADMIN USER', tasks='\u2713Add Administrator'
                                                          '\n\n\u2713View Profile'
                                                          '\n\n\u2713Edit Profile'
                                                          '\n\n\u2713Remove Administrator'
                                                          '\n\n\u2713Pharmacist Dashboard', details='An Administrator can Add New Admins\n'
                                                                                                    ',and Pharmacists, View and Edit their\n'
                                                                                                    'profile information, and can also remove\n'
                                                                                                    'any pharmacist or another administrator.\n'
                                                                                                    'an admin also has pharmacist privileges')
        feature_view_layout.addWidget(admin_info_group)

        user_info_group = Card(title='PHARMACIST', tasks='\u2713Add Medicine'
                                                         '\n\n\u2713View Medicine'
                                                         '\n\n\u2713Edit Medicine'
                                                         '\n\n\u2713Delete Medicine'
                                                         '\n\n\u2713Sell medicine', details='A Pharmacist can add new medicine, \n'
                                                                                            'view and edit medicine information\n'
                                                                                            'delete medicine, view validity stats\n'
                                                                                            'and make sales')
        feature_view_layout.addWidget(user_info_group)

        #  ++++++++++++++++++++++++++++ ADD USER PAGE ++++++++++++++++++++++++

        users_page = QWidget()
        users_page_layout = QVBoxLayout(users_page)
        self.central_widget.addWidget(users_page)

        users_header = Header('Add New User')
        users_page_layout.addWidget(users_header)

        add_user_form = UserForm('create')
        users_page_layout.addWidget(add_user_form)

        #  ++++++++++++++++++++++++++++ VIEW USER PAGE ++++++++++++++++++++++++

        viewer_page = QWidget()
        viewer_page_layout = QVBoxLayout(viewer_page)
        self.central_widget.addWidget(viewer_page)

        viewer_header = QWidget()
        viewer_header.setMaximumHeight(80)
        viewer_header_layout = QHBoxLayout(viewer_header)
        viewer_header_label = Header('View Users')
        viewer_header_layout.addWidget(viewer_header_label)

        refresh_btn = QPushButton('refresh')
        refresh_btn.clicked.connect(update_user_tree)
        refresh_btn.setFont(self.font_normal)
        refresh_btn.setFixedWidth(100)
        viewer_header_layout.addWidget(refresh_btn)

        viewer_page_layout.addWidget(viewer_header)

        user_view = QWidget()
        user_view_layout = QHBoxLayout(user_view)
        viewer_page_layout.addWidget(user_view)

        user_selector = QTreeView()
        self.tree_updater_signal.connect(refetch_tree_data)
        user_selector.clicked.connect(view_profile)
        user_selector.setMaximumWidth(200)
        user_selector.setMaximumHeight(500)
        user_selector_model = QStandardItemModel()
        user_selector.setModel(user_selector_model)
        user_selector_model.setHorizontalHeaderLabels(['User Explorer'])
        user_view_layout.addWidget(user_selector)

        admin_tree = QStandardItem('Administrators')
        admin_tree.setFont(self.font_normal)
        user_selector_model.appendRow(admin_tree)
        db.connect()
        if db.table_exists('users'):
            data = db.fetch_columns('users', 'username', ('role', 'Administrator',))
            for username in data:
                opt = QStandardItem(username[0])
                admin_tree.appendRow(opt)
        else:
            opt_no = QStandardItem('No Admins')
            opt_no.setEnabled(False)
            admin_tree.appendRow(opt_no)

        user_tree = QStandardItem('Pharmacists')
        user_tree.setFont(self.font_normal)
        user_selector_model.appendRow(user_tree)
        if db.table_exists('users'):
            data = db.fetch_columns('users', 'username', ('role', 'Pharmacist',))
            for username in data:
                opt = QStandardItem(username[0])
                user_tree.appendRow(opt)
        else:
            opt_no = QStandardItem('No Pharmacists')
            opt_no.setEnabled(False)
            user_tree.appendRow(opt_no)

        db.close_connection()

        # VIEW USER FORM ++++++++++++++++++
        user_view_layout.addWidget(self.user_view_form)

        #  ++++++++++++++++++++++++++++ ABOUT USER PAGE ++++++++++++++++++++++++

        profile_page = QWidget()
        profile_page_layout = QVBoxLayout(profile_page)

        self.central_widget.addWidget(profile_page)

        profile_header = Header('About The Developer')
        profile_page_layout.addWidget(profile_header)

        dev_info = QGroupBox()
        dev_info.setMaximumHeight(500)
        dev_info_layout = QVBoxLayout(dev_info)
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
