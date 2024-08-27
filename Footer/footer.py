from PySide6.QtWidgets import QGroupBox, QHBoxLayout, QLabel
from PySide6.QtGui import QIcon, QFont
from database import BaseDatabase


class Footer(QGroupBox):
    def __init__(self):
        super().__init__()
        footer_layout = QHBoxLayout()
        self.setLayout(footer_layout)
        self.setFixedHeight(60)
        self.font_bold = QFont('Arial', 14, QFont.Bold)
        db = BaseDatabase('jasphine-pharma-x')

        db.connect()
        if db.table_exists('users'):
            admin_count = db.count_where('users', 'username', ('role', 'Administrator'))
            admin_label = QLabel('  Admins  ')
            admin_label.setFont(self.font_bold)
            admin_label.setMinimumHeight(50)
            admin_label.setEnabled(False)
            footer_layout.addWidget(admin_label)

            pharma_count = db.count_where('users', 'username', ('role', 'Pharmacist'))
            pharm_label = QLabel(' Pharmacists ')
            pharm_label.setFont(self.font_bold)
            pharm_label.setMinimumHeight(50)
            pharm_label.setEnabled(False)
            footer_layout.addWidget(pharm_label)
        else:
            admin_label = QLabel(' Register Admins')
            admin_label.setFont(self.font_bold)
            admin_label.setMinimumHeight(50)
            admin_label.setEnabled(False)
            footer_layout.addWidget(admin_label)

            pharm_label = QLabel(' Register Pharmacists')
            pharm_label.setFont(self.font_bold)
            pharm_label.setMinimumHeight(50)
            pharm_label.setEnabled(False)
            footer_layout.addWidget(pharm_label)
        db.close_connection()

