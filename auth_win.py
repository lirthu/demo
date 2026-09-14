import sys


from PyQt6.QtWidgets import QDialog, QApplication, QPushButton, QLineEdit, QMessageBox
from PyQt6.uic import loadUi

from catalog_win import CatalogWin


c = connection.cursor()

class AuthWin(QDialog):
    login_btn: QPushButton
    guest_btn: QPushButton
    login_line = QLineEdit
    password_line = QLineEdit
    def __init__(self):
        super().__init__()
        loadUi('ui\\auth.ui', self)
        self.login_btn.clicked.connect(self.login_auth)
        self.guest_btn.clicked.connect(self.login_guest)

    def login_auth(self):
        login = self.login_line.text()
        password = self.password_line.text()
        if not login or not password:
            QMessageBox.warning(self, 'Внимание!', 'Заполните все поля')
        else:
            c.execute('SELECT * FROM users WHERE login = %s and password = %s', (login, password,))
            res = c.fetchone()
            if res:
                self.close()
                self.win = CatalogWin(id=res[0])
                self.win.show()
            else:
                QMessageBox.warning(self, 'Ошибка', 'Неверный логин или пароль!')

    def login_guest(self):
        try:
            self.close()
            self.win = CatalogWin()
            self.win.show()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AuthWin()
    win.show()
    sys.exit(app.exec())
