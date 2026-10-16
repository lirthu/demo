import sys

from PyQt6.QtWidgets import QDialog, QApplication, QPushButton
from PyQt6.uic import loadUi


class OrderWin(QDialog):
    return_btn: QPushButton
    def __init__(self):
        super().__init__()
        loadUi('ui\\order_win.ui', self)
        self.return_btn.clicked.connect(self.return_to_items)

    def return_to_items(self):
        from catalog_win import CatalogWin
        self.win = CatalogWin()
        self.win.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = OrderWin()
    win.show()
    sys.exit(app.exec())
