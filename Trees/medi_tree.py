from PySide6.QtWidgets import QTreeView
from PySide6.QtGui import QStandardItem, QStandardItemModel, QFont
from database import BaseDatabase
import datetime

db = BaseDatabase('jasphine-pharma-x')


class MediTree(QTreeView):
    def __init__(self, clicked):
        super().__init__()
        self.clicked.connect(clicked)
        self.setMaximumWidth(200)
        self.setMinimumHeight(500)
        self.font_normal = QFont('Arial', 10)

        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.model.setHorizontalHeaderLabels(['Medicine Explorer'])

        expired_tree = QStandardItem('Expired medicine')
        expired_tree.setFont(self.font_normal)
        self.model.appendRow(expired_tree)

        valid_tree = QStandardItem('Valid medicine')
        valid_tree.setFont(self.font_normal)
        self.model.appendRow(valid_tree)

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
                if formated_exp < formated_now:
                    valid_medicine.append(medicine[0])
                else:
                    expired_medicine.append(medicine[0])

        db.close_connection()

        if valid_medicine:
            for valid in valid_medicine:
                option = QStandardItem(valid)
                expired_tree.appendRow(option)
        else:
            no1 = QStandardItem('no expired')
            no1.setEnabled(False)
            expired_tree.appendRow(no1)

        if expired_medicine:
            for expired in expired_medicine:
                option2 = QStandardItem(expired)
                valid_tree.appendRow(option2)
        else:
            no2 = QStandardItem('no valid')
            no2.setEnabled(False)
            valid_tree.appendRow(no2)

    def get_model(self):
        return self.model
