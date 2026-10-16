import sys

from PyQt6.QtMultimedia import QMediaMetaData
from PyQt6.QtWidgets import QDialog, QApplication, QPushButton, QMessageBox
from PyQt6.uic import loadUi


class OrderWin(QDialog):
    return_btn: QPushButton
    def __init__(self, user):
        super().__init__()
        self.user = user
        loadUi('ui\\order_win.ui', self)
        self.return_btn.clicked.connect(self.return_to_items)
        self.add_item_btn.clicked.connect(self.open_add_odred_win)

    def return_to_items(self):
        from catalog_win import CatalogWin
        self.win = CatalogWin(self.user)
        self.win.show()
        self.close()

    def open_add_odred_win(self, order_id=None):
        try:
            from add_order_win import AddOrderWin
            from db_servives import DB_service
            win = AddOrderWin(order_id)
            win.show()
            # if win.exec() == QDialog.DialogCode.Accepted:
                # db = DB_service()
                # if order_id is None:
                #     db.save_order(*win.result)
                # else:
                #     db.update_order(*win.result)
            # self.refresh_orders()
        except Exception as error:
            QMessageBox.warning(self, 'Ошибка открытия окна', f'Ошибка: {error}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = OrderWin()
    win.show()
    sys.exit(app.exec())
