import time

from PySide6.QtWidgets import (QLabel, QLineEdit, QDateEdit, QSpinBox,
                               QGroupBox, QHBoxLayout, QVBoxLayout, QWidget)
from PySide6.QtGui import QFont
from Buttons.click_button import ClickButton
from database import BaseDatabase
from PySide6.QtCore import Signal
from state_manager import state_manager


class MedicalForm(QGroupBox):
    set_data = Signal()

    def __init__(self, action: str, data: dict = None):
        if data is None:
            data = {'name': '',
                    'description': '',
                    'mfg': '',
                    'exp': '',
                    'qty': '',
                    'price': ''}
        self.action = action
        self.data = data

        super().__init__()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setFixedHeight(500)
        self.font_normal = QFont('Arial', 10)

        db = BaseDatabase('jasphine-pharma-x')

        #  ++++++++++++++++++++++++++ FUNCTIONS ++++++++++++++++++++++++

        def set_form_data():
            selected_medicine = state_manager.get_states('selected_medicine')
            db.connect()
            medicine_info = db.fetch_row('medicine', ('name', selected_medicine,))
            db.close_connection()
            medi_dict = {
                'name': medicine_info[1],
                'description': medicine_info[2],
                'mfg': medicine_info[3],
                'expiry': medicine_info[4],
                'quantity': medicine_info[5],
                'unit_cost': medicine_info[6]
            }
            name_input.setText(medi_dict.get('name'))
            description_input.setText(medi_dict.get('description'))
            quantity_input.setValue(int(medi_dict.get('quantity')))
            price_input.setText(medi_dict.get('unit_cost'))

        self.set_data.connect(set_form_data)

        def save_new():
            medi_name = name_input.text()
            medi_desc = description_input.text()
            medi_mfg = date_input.text()
            medi_exp = expiry_date_input.text()
            quantity = quantity_input.text()
            unit_cost = price_input.text()
            if len(medi_mfg) and len(medi_exp) == 10:
                if len(medi_name) > 3 and len(unit_cost) >=1:
                    medi_dict = {
                        'name': medi_name,
                        'description': medi_desc,
                        'mfg': medi_mfg,
                        'expiry': medi_exp,
                        'quantity': quantity,
                        'unit_cost': unit_cost
                    }
                    db.connect()
                    if db.table_exists('medical'):
                        db.insert_data('medical', medi_dict)
                        db.commit_changes()
                    else:
                        columns_dict = {
                            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                            'name': 'TEXT NOT NULL',
                            'description': 'TEXT NOT NULL',
                            'mfg': 'TEXT NOT NULL',
                            'expiry': 'TEXT NOT NULL',
                            'quantity': 'TEXT NOT NULL',
                            'unit_cost': 'TEXT NOT NULL'
                        }
                        db.create_table('medical', columns_dict)
                        db.insert_data('medical', medi_dict)
                        db.commit_changes()
                    db.close_connection()
                    clear_entries()
                    error.setText('')
                else:
                    error.setText('short name or invalid unit cost')
            else:
                error.setText('invalid date(s)')

        def clear_entries():
            name_input.clear()
            description_input.clear()
            date_input.clear()
            expiry_date_input.clear()
            quantity_input.clear()
            price_input.clear()

        def update_medicine():
            medi_name = name_input.text()
            medi_desc = description_input.text()
            medi_mfg = date_input.text()
            medi_exp = expiry_date_input.text()
            quantity = quantity_input.text()
            unit_cost = price_input.text()
            if len(medi_exp) and len(medi_mfg) == 10:
                if len(medi_name) > 3 and len(quantity) and len(unit_cost) >= 1:

                    medi_dict = {
                        'name': medi_name,
                        'description': medi_desc,
                        'mfg': medi_mfg,
                        'expiry': medi_exp,
                        'quantity': quantity,
                        'unit_cost': unit_cost
                    }
                    db.connect()
                    db.update_data('medical', medi_dict, ('name', self.selected_view))
                    db.commit_changes()
                    db.close_connection()
                    disable_entries()
                else:
                    pass
                    # viewer_header.set_text('short name or empty values')
            else:
                pass
                # viewer_header.set_text('invalid date(s)')

        def disable_entries():
            name_input.setEnabled(False)
            description_input.setEnabled(False)
            date_input.setEnabled(False)
            expiry_date_input.setEnabled(False)
            quantity_input.setEnabled(False)
            price_input.setEnabled(False)

        def enable_entries():
            name_input.setEnabled(True)
            description_input.setEnabled(True)
            date_input.setEnabled(True)
            expiry_date_input.setEnabled(True)
            quantity_input.setEnabled(True)
            price_input.setEnabled(True)

        def disable_buttons():
            button_holder.setEnabled(False)
            # action_holder.setEnabled(False)

        def enable_buttons():
            button_holder.setEnabled(True)
            # action_holder.setEnabled(True)

        def edit_data():
            enable_entries()

        def delete_medicine():
            db.connect()
            db.delete_row('medical', ('name', self.selected_view))
            db.commit_changes()
            db.close_connection()
            clear_entries()
            disable_entries()
            disable_buttons()
            # item = medi_view_selector_model.indexFromItem(self.selected_view)
            # item_index = item.row()
            # medi_view_selector_model.removeRow(item_index)
            # medi_view_selector.setModel(medi_view_selector_model)
            # medi_view_selector.repaint()

        # ++++++++++++++++++++++++++ FORM LEFT SECTION +++++++++++++++++++

        left_section = QWidget()
        left_section_layout = QVBoxLayout()
        left_section.setLayout(left_section_layout)
        self.layout.addWidget(left_section)

        error = QLabel('')
        self.layout.addWidget(error)

        name_holder = QWidget()
        name_holder.setMaximumHeight(80)
        name_holder.setMaximumWidth(500)
        name_holder_layout = QVBoxLayout()
        name_holder.setLayout(name_holder_layout)
        left_section_layout.addWidget(name_holder)
        name_label = QLabel('Medicine Name')
        name_label.setFont(self.font_normal)
        name_holder_layout.addWidget(name_label)
        name_input = QLineEdit(self.data.get('name'))
        name_input.setFont(self.font_normal)
        name_holder_layout.addWidget(name_input)

        description_holder = QWidget()
        description_holder.setMaximumHeight(80)
        description_holder.setMaximumWidth(500)
        description_holder_layout = QVBoxLayout()
        description_holder.setLayout(description_holder_layout)
        left_section_layout.addWidget(description_holder)
        description_label = QLabel('Description')
        description_label.setFont(self.font_normal)
        description_holder_layout.addWidget(description_label)
        description_input = QLineEdit(self.data.get('description'))
        description_input.setFont(self.font_normal)
        description_holder_layout.addWidget(description_input)

        date_holder = QWidget()
        date_holder.setMaximumWidth(500)
        date_holder.setMaximumHeight(80)
        date_holder_layout = QVBoxLayout()
        date_holder.setLayout(date_holder_layout)
        left_section_layout.addWidget(date_holder)
        date_label = QLabel('Manufactured Date')
        date_label.setFont(self.font_normal)
        date_holder_layout.addWidget(date_label)
        date_input = QDateEdit(self.data.get('mfg'))
        date_input.setDisplayFormat('dd/MM/yyyy')
        date_input.setFont(self.font_normal)
        date_holder_layout.addWidget(date_input)

        expiry_date_holder = QWidget()
        expiry_date_holder.setMaximumWidth(500)
        expiry_date_holder.setMaximumHeight(80)
        expiry_date_holder_layout = QVBoxLayout()
        expiry_date_holder.setLayout(expiry_date_holder_layout)
        left_section_layout.addWidget(expiry_date_holder)
        expiry_date_label = QLabel('Expiry Date')
        expiry_date_label.setFont(self.font_normal)
        expiry_date_holder_layout.addWidget(expiry_date_label)
        expiry_date_input = QDateEdit(self.data.get('exp'))
        expiry_date_input.setDisplayFormat('dd/MM/yyyy')
        expiry_date_input.setFont(self.font_normal)
        expiry_date_holder_layout.addWidget(expiry_date_input)

        # ++++++++++++++++++++++++++ FORM RIGHT SECTION +++++++++++++++++++

        right_section = QWidget()
        right_section_layout = QVBoxLayout()
        right_section.setLayout(right_section_layout)
        self.layout.addWidget(right_section)

        quantity_holder = QWidget()
        quantity_holder.setMaximumWidth(500)
        quantity_holder.setMaximumHeight(80)
        quantity_holder_layout = QVBoxLayout()
        quantity_holder.setLayout(quantity_holder_layout)
        quantity_label = QLabel('Quantity')
        quantity_label.setFont(self.font_normal)
        quantity_holder_layout.addWidget(quantity_label)
        quantity_input = QSpinBox()
        quantity_input.setValue(int(self.data.get('qty')))
        quantity_input.setFont(self.font_normal)
        quantity_holder_layout.addWidget(quantity_input)
        right_section_layout.addWidget(quantity_holder)

        price_holder = QWidget()
        price_holder.setMaximumWidth(500)
        price_holder.setMaximumHeight(80)
        price_holder_layout = QVBoxLayout()
        price_holder.setLayout(price_holder_layout)
        price_label = QLabel('Unit Price')
        price_label.setFont(self.font_normal)
        price_holder_layout.addWidget(price_label)
        price_input = QLineEdit(self.data.get('price'))
        price_input.setFont(self.font_normal)
        price_holder_layout.addWidget(price_input)
        right_section_layout.addWidget(price_holder)

        button_holder = QWidget()
        button_holder.setMaximumWidth(500)
        button_holder.setMaximumHeight(160)
        button_holder_layout = QHBoxLayout()
        button_holder.setLayout(button_holder_layout)

        if self.action == 'create':
            button_save = ClickButton('Save', save_new)
            button_holder_layout.addWidget(button_save)

            button_clear = ClickButton('Clear', clear_entries)
            button_holder_layout.addWidget(button_clear)

            right_section_layout.addWidget(button_holder)
        elif self.action == 'edit':
            button_edit = ClickButton('Edit', save_new)
            button_holder_layout.addWidget(button_edit)

            button_delete = ClickButton('Delete', clear_entries)
            button_holder_layout.addWidget(button_delete)

            button_save = ClickButton('Save Changes', save_new)
            button_holder_layout.addWidget(button_save)

            button_clear = ClickButton('Clear', clear_entries)
            button_holder_layout.addWidget(button_clear)

            right_section_layout.addWidget(button_holder)
        else:
            pass
