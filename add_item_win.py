import sys

from PyQt6.QtWidgets import QApplication, QDialog, QComboBox
from PyQt6.uic import loadUi


class AddItemWindow(QDialog):
    filter_box: QComboBox
    dealer_box: QComboBox

    def __init__(self):
        super().__init__()
        loadUi('ui\\add_item.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AddItemWindow()
    win.show()
    sys.exit(app.exec())