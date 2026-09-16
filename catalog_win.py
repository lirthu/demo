import sys

from PyQt6.QtWidgets import QDialog, QApplication, QPushButton
from PyQt6.uic import loadUi


class CatalogWin(QDialog):
    exit_btn: QPushButton
    def __init__(self, user):
        super().__init__()
        loadUi('ui\\catalog_win.ui',self)
        self.exit_btn.clicked.connect(self.exit_app)

    def exit_app(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = CatalogWin()
    win.show()
    sys.exit(app.exec())
