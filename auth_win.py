import sys

from PyQt6.QtWidgets import QDialog, QApplication, QPushButton, QLineEdit, QMessageBox
from PyQt6.uic import loadUi

from catalog_win import CatalogWin
from db_servives import DB_service


class AuthWin(QDialog):
    login_btn: QPushButton
    guest_btn: QPushButton
    login_line = QLineEdit
    password_line = QLineEdit
    def __init__(self):
        super().__init__()
        loadUi('ui\\auth.ui', self)
        self.login_btn.clicked.connect(self.login_auth)
        self.guest_btn.clicked.connect(self.open_catalog_window)

    def login_auth(self):
        login = self.login_line.text().strip()
        password = self.password_line.text().strip()
        if not login or not password:
            QMessageBox.warning(self, 'Внимание!', 'Заполните все поля')
        user = DB_service().get_user_info(login, password)
        if user:
            return self.open_catalog_window(user)
        return None

    def open_catalog_window(self, user=None):
        from catalog_win import CatalogWin
        self.win = CatalogWin(user)
        self.win.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AuthWin()
    win.show()
    sys.exit(app.exec())
