from PySide6.QtWidgets import (QLabel, QLineEdit, QComboBox,
                               QGroupBox, QHBoxLayout, QVBoxLayout, QWidget)
from PySide6.QtGui import QFont
from database import BaseDatabase
from state_manager import state_manager
from Buttons.click_button import ClickButton
from PySide6.QtCore import Signal


class UserForm(QGroupBox):
    set_data = Signal(str)

    def __init__(self, action, data={'role': '', 'name': '', 'username': '', 'dob': '', 'contact': '', 'email': '', 'password': ''}):
        self.action = action
        self.data = data

        super().__init__()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setFixedHeight(500)
        self.font_normal = QFont('Arial', 10)

        db = BaseDatabase('jasphine-pharma-x')

        # +++++++++++++++++++++++++ FUNCTIONS +++++++++++++++++++++++++++

        def set_form_data(current_profile):
            db.connect()
            profile_data = db.fetch_row('users', ('username', current_profile,))
            data_dict = {'role': profile_data[1],
                         'name': profile_data[2],
                         'username': profile_data[3],
                         'contact': profile_data[4],
                         'email': profile_data[5],
                         'password': profile_data[6]}
            role_input.setCurrentText(data_dict['role'])
            name_input.setText(data_dict['name'])
            user_name_input.setText(data_dict['username'])
            contact_input.setText(data_dict['contact'])
            email_input.setText(data_dict['email'])
            password_input.setText(data_dict['password'])
            enable_buttons()

        self.set_data.connect(set_form_data)

        def validate():
            error = ''
            name = name_input.text()
            user_name = user_name_input.text()
            phone_number = contact_input.text()
            email = email_input.text()
            password = password_input.text()
            if len(name) <= 3:
                error = 'empty or too short name'
                name_input.setText(error)
                return False
            elif len(user_name) <= 3:
                error = 'empty or too short username'
                user_name_input.setText(error)
                return False
            elif len(phone_number) < 10:
                error = 'too short phone number'
                contact_input.setText(error)
                return False
            elif not '@' in email:
                error = 'invalid email'
                email_input.setText(error)
                return False
            elif len(password) < 8:
                error = 'password should be 8 characters or more'
                password_input.setText(error)
                return False
            else:
                return True

        def save_data(mode: int = 0):
            validation = validate()
            if validation:
                role = role_input.currentText()
                name = name_input.text()
                user_name = user_name_input.text()
                phone_number = contact_input.text()
                email = email_input.text()
                password = password_input.text()

                data_dict = {
                    'role': role,
                    'fullname': name,
                    'username': user_name,
                    'contact': phone_number,
                    'email': email,
                    'encryption': password
                }
                columns_dict = {
                    'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                    'role': 'TEXT NOT NULL',
                    'fullname': 'TEXT NOT NULL',
                    'username': 'TEXT NOT NULL',
                    'contact': 'TEXT NOT NULL',
                    'email': 'TEXT NOT NULL',
                    'encryption': 'TEXT NOT NULL'
                }

                db.connect()
                if db.table_exists('users'):
                    db.insert_data('users', data_dict)
                    db.commit_changes()
                    db.close_connection()
                else:
                    db.create_table('users', columns_dict=columns_dict)
                    db.insert_data('users', data_dict)
                    db.commit_changes()
                    db.close_connection()

                if mode == 0:
                    clear_entries()
                else:
                    disable_entries()
            else:
                pass

        def edit_data():
            enable_entries()

        def update_data():
            validation = validate()
            selected_user = state_manager.get_states('selected_user')
            if validation:
                role = role_input.currentText()
                name = name_input.text()
                user_name = user_name_input.text()
                phone_number = contact_input.text()
                email = email_input.text()
                password = password_input.text()

                data_dict = {
                    'role': role,
                    'fullname': name,
                    'username': user_name,
                    'contact': phone_number,
                    'email': email,
                    'encryption': password
                }
                db.connect()
                db.update_data('users', data_dict, ('username', selected_user))
                db.commit_changes()
                db.close_connection()
                disable_entries()
                disable_buttons()
            else:
                pass

        def delete_selection():
            db.connect()
            db.delete_row('users', ('username', user_name_input.text()))
            clear_entries()

        def clear_entries():
            role_input.setCurrentIndex(0)
            name_input.clear()
            user_name_input.clear()
            contact_input.clear()
            email_input.clear()
            password_input.clear()

        def disable_entries():
            role_input.setEnabled(False)
            name_input.setEnabled(False)
            user_name_input.setEnabled(False)
            contact_input.setEnabled(False)
            email_input.setEnabled(False)
            password_input.setEnabled(False)

        def enable_entries():
            role_input.setEnabled(True)
            name_input.setEnabled(True)
            user_name_input.setEnabled(True)
            contact_input.setEnabled(True)
            email_input.setEnabled(True)
            password_input.setEnabled(True)

        def disable_buttons():
            button_holder.setEnabled(False)

        def enable_buttons():
            action_holder.setEnabled(True)
            button_holder.setEnabled(True)

        # ++++++++++++++++++++++++++ FORM LEFT SECTION +++++++++++++++++++
        left_section = QWidget()
        left_section_layout = QVBoxLayout()
        left_section.setLayout(left_section_layout)
        self.layout.addWidget(left_section)

        role_holder = QWidget()
        role_holder.setMaximumHeight(80)
        role_holder.setMaximumWidth(500)
        role_holder_layout = QVBoxLayout()
        role_holder.setLayout(role_holder_layout)
        left_section_layout.addWidget(role_holder)
        role_label = QLabel('User Role')
        role_label.setFont(self.font_normal)
        role_holder_layout.addWidget(role_label)
        role_input = QComboBox()
        role_input.setFont(self.font_normal)
        role_input.addItems(['Administrator', 'Pharmacist'])
        role_holder_layout.addWidget(role_input)

        name_holder = QWidget()
        name_holder.setMaximumHeight(80)
        name_holder.setMaximumWidth(500)
        name_holder_layout = QVBoxLayout()
        name_holder.setLayout(name_holder_layout)
        left_section_layout.addWidget(name_holder)
        name_label = QLabel('Full Name')
        name_label.setFont(self.font_normal)
        name_holder_layout.addWidget(name_label)
        name_input = QLineEdit(self.data.get('name'))
        name_input.setFont(self.font_normal)
        name_holder_layout.addWidget(name_input)

        user_name_holder = QWidget()
        user_name_holder.setMaximumHeight(80)
        user_name_holder.setMaximumWidth(500)
        user_name_holder_layout = QVBoxLayout()
        user_name_holder.setLayout(user_name_holder_layout)
        left_section_layout.addWidget(user_name_holder)
        user_name_label = QLabel('User Name')
        user_name_label.setFont(self.font_normal)
        user_name_holder_layout.addWidget(user_name_label)
        user_name_input = QLineEdit(self.data.get('username'))
        user_name_input.setFont(self.font_normal)
        user_name_holder_layout.addWidget(user_name_input)

        contact_holder = QWidget()
        contact_holder.setMaximumWidth(500)
        contact_holder.setMaximumHeight(80)
        contact_holder_layout = QVBoxLayout()
        contact_holder.setLayout(contact_holder_layout)
        contact_label = QLabel('Phone Number')
        contact_label.setFont(self.font_normal)
        contact_holder_layout.addWidget(contact_label)
        contact_input = QLineEdit(self.data.get('contact'))
        contact_input.setFont(self.font_normal)
        contact_holder_layout.addWidget(contact_input)
        left_section_layout.addWidget(contact_holder)

        # ++++++++++++++++++++++++++ FORM RIGHT SECTION +++++++++++++++++++
        right_section = QWidget()
        right_section_layout = QVBoxLayout()
        right_section.setLayout(right_section_layout)
        self.layout.addWidget(right_section)

        email_holder = QWidget()
        email_holder.setMaximumWidth(500)
        email_holder.setMaximumHeight(80)
        email_holder_layout = QVBoxLayout()
        email_holder.setLayout(email_holder_layout)
        email_label = QLabel('Email Address')
        email_label.setFont(self.font_normal)
        email_holder_layout.addWidget(email_label)
        email_input = QLineEdit(self.data.get('email'))
        email_input.setFont(self.font_normal)
        email_holder_layout.addWidget(email_input)
        right_section_layout.addWidget(email_holder)

        password_holder = QWidget()
        password_holder.setMaximumWidth(500)
        password_holder.setMaximumHeight(80)
        password_holder_layout = QVBoxLayout()
        password_holder.setLayout(password_holder_layout)
        password_label = QLabel('Password')
        password_label.setFont(self.font_normal)
        password_holder_layout.addWidget(password_label)
        password_input = QLineEdit(self.data.get('password'))
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setFont(self.font_normal)
        password_holder_layout.addWidget(password_input)
        right_section_layout.addWidget(password_holder)

        if self.action == 'create':
            button_holder = QWidget()
            button_holder.setMaximumWidth(500)
            button_holder.setMaximumHeight(160)
            button_holder_layout = QHBoxLayout()
            button_holder.setLayout(button_holder_layout)
            right_section_layout.addWidget(button_holder)

            button_save = ClickButton('Save', save_data)
            button_holder_layout.addWidget(button_save)

            button_clear = ClickButton('Clear', clear_entries)
            button_holder_layout.addWidget(button_clear)
        elif self.action == 'edit':
            disable_entries()
            action_holder = QWidget()
            action_holder.setMaximumWidth(500)
            action_holder.setMaximumHeight(80)
            action_holder_layout = QHBoxLayout()
            action_holder.setLayout(action_holder_layout)
            right_section_layout.addWidget(action_holder)

            action_edit = ClickButton('Edit', edit_data)
            action_holder_layout.addWidget(action_edit)

            action_delete = ClickButton('Delete', delete_selection)
            action_holder_layout.addWidget(action_delete)

            button_holder = QWidget()
            button_holder.setMaximumWidth(500)
            button_holder.setMaximumHeight(80)
            button_holder_layout = QHBoxLayout()
            button_holder.setLayout(button_holder_layout)
            right_section_layout.addWidget(button_holder)

            button_save = ClickButton('Save Changes', update_data)
            button_holder_layout.addWidget(button_save)

            button_clear = ClickButton('Clear', clear_entries)
            button_holder_layout.addWidget(button_clear)
        else:
            pass
