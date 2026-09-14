import sys

from PyQt6.QtWidgets import QDialog, QApplication
from PyQt6.uic import loadUi


class CatalogWin(QDialog):
    def __init__(self, id):
        super().__init__()
        loadUi('ui\\catalog_win.ui')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = CatalogWin()
    win.show()
    sys.exit(app.exec())
