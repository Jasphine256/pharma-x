from PySide6.QtWidgets import QTableView
from PySide6.QtGui import QStandardItemModel, QStandardItem


class DataTable(QTableView):
    def __init__(self, data_frame):
        super().__init__()

        # Convert DataFrame to QStandardItemModel
        self.model = self.data_frame_to_modal(data_frame)

        # Set the model to the table view
        self.setModel(self.model)

        self.setEnabled(False)

    def data_frame_to_modal(self, data_frame):
        model = QStandardItemModel(data_frame.shape[0], data_frame.shape[1])
        model.setHorizontalHeaderLabels(data_frame.columns)

        for row in range(data_frame.shape[0]):
            for column in range(data_frame.shape[1]):
                item = QStandardItem(str(data_frame.iloc[row, column]))
                model.setItem(row, column, item)

        return model
