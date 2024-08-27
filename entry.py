from PySide6.QtWidgets import QWidget, QDialog, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QGroupBox, QLineEdit
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from database import BaseDatabase
from admin import AdminWindow
from user import UserWindow
from qtmodern import windows as win
from state_manager import state_manager
import sys
import os

db = BaseDatabase('jasphine-pharma-x')


class EntryWindow(QDialog):
    user = 'CHOOSE USER TYPE'

    def __init__(self):
        super().__init__()
        self.setFixedWidth(700)
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        self.images_dir = ''
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle (e.g. PyInstaller)
            self.images_dir = os.path.join(sys._MEIPASS, 'images')
        else:
            # If the application is run from the script directly
            self.images_dir = os.path.join(os.path.abspath("."), 'images')
        self.initUI()

    def initUI(self):
        side_bar = QWidget()
        side_bar.setFixedWidth(250)
        side_bar_layout = QVBoxLayout()
        side_bar.setLayout(side_bar_layout)
        self.main_layout.addWidget(side_bar)
        self.setGeometry(300, 100, 0, 0)

        # +++++++++++++++++++++++ FUNCTIONS +++++++++++++++++++++++

        def as_admin():
            self.set_user('ADMINISTRATOR')
            login_group.setTitle(self.user)
            name_entry.setText('Admin')

        def as_user():
            self.set_user('PHARMACIST')
            login_group.setTitle(self.user)
            name_entry.setText('Enter User Name')

        def login():
            username = name_entry.text().strip()
            password = password_entry.text()
            if self.user == 'ADMINISTRATOR':
                db.connect()
                if db.table_exists('users'):
                    credentials = db.fetch_row('users', ('username', username))
                    if not credentials is None:
                        role = credentials[1]
                        passkey = credentials[-1]
                        if role == "Administrator" and password == passkey:
                            state_manager.set_state('username', username)
                            self.wind = AdminWindow()
                            mw = win.ModernWindow(self.wind)
                            mw.showMaximized()
                            self.accept()
                        else:
                            name_entry.setText('Invalid Password or not admin')
                    else:
                        name_entry.setText('Invalid Username')
                else:
                    if username == 'Admin' and password == 'password':
                        self.wind = AdminWindow()
                        mw = win.ModernWindow(self.wind)
                        mw.showMaximized()
            elif self.user == 'PHARMACIST':
                db.connect()
                if db.table_exists('users'):
                    credentials = db.fetch_row('users', ('username', username))
                    if not credentials is None:
                        passkey = credentials[-1]
                        if password == passkey:
                            state_manager.set_state('username', username)
                            self.wind = UserWindow()
                            mw = win.ModernWindow(self.wind)
                            mw.showMaximized()
                            self.accept()
                        else:
                            name_entry.setText('Invalid Password')
                    else:
                        name_entry.setText('Invalid Username')
                else:
                    name_entry.setText('No pharmacists')
            else:
                name_entry.setText('Please choose type of user')

        # ++++++++++++++++ USER INTERFACE DESIGN +++++++++++++++++=

        admin_image = QPixmap(os.path.join(self.images_dir, 'login.png')).scaled(200, 200, aspectMode=Qt.AspectRatioMode.KeepAspectRatio)
        admin_image_label = QLabel()
        admin_image_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        admin_image_label.setMaximumWidth(300)
        admin_image_label.setPixmap(admin_image)
        side_bar_layout.addWidget(admin_image_label)

        login_label = QLabel('LOGIN AS')
        login_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        side_bar_layout.addWidget(login_label)

        chooser_group = QGroupBox()
        chooser_group_layout = QHBoxLayout()
        chooser_group.setLayout(chooser_group_layout)
        side_bar_layout.addWidget(chooser_group)

        login_as_admin = QPushButton("Administrator")
        login_as_admin.setProperty('class', 'selector-login-btn')
        login_as_admin.clicked.connect(as_admin)
        login_as_user = QPushButton("  Pharmacist  ")
        login_as_user.setProperty('class', 'selector-login-btn')
        login_as_user.clicked.connect(as_user)
        chooser_group_layout.addWidget(login_as_admin)
        chooser_group_layout.addWidget(login_as_user)

        login_view = QWidget()
        login_view_layout = QVBoxLayout()
        login_view.setLayout(login_view_layout)
        self.main_layout.addWidget(login_view)

        login_group = QGroupBox()
        login_group.setObjectName('login-groupbox')
        login_group.setFixedHeight(300)
        login_group.setTitle(self.user)
        login_group_layout = QVBoxLayout()
        login_group.setLayout(login_group_layout)
        login_view_layout.addWidget(login_group)

        holder_layout1 = QHBoxLayout()
        name_label = QLabel('Username')
        name_entry = QLineEdit()
        holder_layout1.addWidget(name_label)
        holder_layout1.addWidget(name_entry)

        holder_layout2 = QHBoxLayout()
        password_label = QLabel('Password')
        password_entry = QLineEdit()
        password_entry.setEchoMode(QLineEdit.Password)
        holder_layout2.addWidget(password_label)
        holder_layout2.addWidget(password_entry)

        login_button = QPushButton("Login")
        login_button.setProperty('class', 'login-btn')
        login_button.clicked.connect(login)

        login_group_layout.addLayout(holder_layout1)
        login_group_layout.addLayout(holder_layout2)
        login_group_layout.addWidget(login_button)

    def set_user(self, name: str):
        self.user = name
