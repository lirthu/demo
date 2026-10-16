import sys

from PyQt6.QtWidgets import QDialog, QApplication, QPushButton, QMessageBox
from PyQt6.uic import loadUi
from db_servives import DB_service

class AddOrderWin(QDialog):
    return_btn: QPushButton
    delete_btn: QPushButton
    def __init__(self, order_id = None):
        super().__init__()
        loadUi('ui\\add_order.ui', self)
        self.order_id = order_id
        if self.order_id is None:
            self.delete_btn.hide()
        else:
            self.delete_btn.clicked.connect(self.delete_order)
            self.load_order(self.order_id)

    def show_dealers(self):
        self.user_box.addItem('Выберете клиента')
        for sid, sname in DB_service().get_users():
            self.user_box.addItem(sname, sid)

    def show_creators(self):
        self.creator_box.addItem('Выберете Производителя')
        for sid, sname in DB_service().get_creators():
            self.creator_box.addItem(sname, sid)

    def load_order(self, order_id):
        db = DB_service()
        row = db.get_order_by_id()

    def delete_order(self):
        from db_servives import DB_service
        db = DB_service()
        answer = QMessageBox.question(
            self, 'Удаление',
            'Вы уверены, что хотите удалить заказ?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if answer == QMessageBox.StandardButton.Yes:
            db.delete_order(self.order_id)
            self.reject()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AddOrderWin()
    win.show()
    sys.exit(app.exec())
