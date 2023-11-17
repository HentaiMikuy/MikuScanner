from PySide6.QtWidgets import QTableWidgetItem
from qfluentwidgets import TableWidget


class TableFrame(TableWidget):

    def __init__(self, portInfos,parent=None):
        super().__init__(parent)
        self.dataInfos = portInfos

        self.verticalHeader().hide()
        self.setBorderRadius(8)
        self.setBorderVisible(True)

        self.setColumnCount(3)
        self.setRowCount(len(portInfos))
        self.setHorizontalHeaderLabels([
            'Port', 'Status', 'Service Name'
        ])

        self.dataInfos += self.dataInfos
        for i, Info in enumerate(self.dataInfos):
            for j in range(3):
                self.setItem(i, j, QTableWidgetItem(Info[j]))

        self.setFixedSize(407, 124)
        self.resizeColumnsToContents()