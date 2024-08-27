from PySide6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QLabel
from PySide6.QtGui import QFont


class Card(QGroupBox):
    def __init__(self, title, tasks, details):
        self.title = title
        self.tasks = tasks
        self.details = details
        self.font_normal = QFont('Arial', 10)
        super().__init__()
        self.setTitle(self.title)
        self.setFixedHeight(400)
        self.admin_info_group_layout = QVBoxLayout()
        self.setLayout(self.admin_info_group_layout)

        self.initUI()

    def initUI(self):
        admin_inner_group1 = QWidget()
        admin_inner_group1.setFixedWidth(200)
        admin_inner_group1_layout = QVBoxLayout()
        admin_inner_group1.setLayout(admin_inner_group1_layout)
        self.admin_info_group_layout.addWidget(admin_inner_group1)

        admin_tasks_label = QLabel(self.tasks)
        admin_tasks_label.setFont(self.font_normal)
        admin_inner_group1_layout.addWidget(admin_tasks_label)

        admin_inner_group2 = QWidget()
        admin_inner_group2_layout = QVBoxLayout()
        admin_inner_group2.setLayout(admin_inner_group2_layout)
        self.admin_info_group_layout.addWidget(admin_inner_group2)

        admin_info_label = QLabel(self.details)
        admin_info_label.setFont(self.font_normal)
        admin_inner_group2_layout.addWidget(admin_info_label)
