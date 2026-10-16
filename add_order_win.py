import sys

from PyQt6.QtWidgets import QDialog, QApplication, QPushButton, QMessageBox, QComboBox
from PyQt6.uic import loadUi
from db_servives import DB_service

class AddOrderWin(QDialog):
    return_btn: QPushButton
    delete_btn: QPushButton
    cancel: QPushButton
    user_box: QComboBox
    giver_box: QComboBox
    item_box: QComboBox
    def __init__(self, order_id = None):
        super().__init__()
        loadUi('ui\\add_order.ui', self)
        self.order_id = order_id
        if self.order_id is None:
            self.delete_btn.hide()
        else:
            self.delete_btn.clicked.connect(self.delete_order)
            self.load_order(self.order_id)

        self.cancel.clicked.connect(self.reject)

        self.show_users()
        self.show_givers()
        self.show_items()

    # блок добавления

    def show_users(self):
        self.user_box.addItem('Выберете клиента', None)
        for id, name, surename, role in DB_service().get_users():
            self.user_box.addItem(f'{surename} {name}: {role}', id)

    def show_givers(self):
        self.giver_box.addItem('Выберете производителя', None)
        for id, g_index, name in DB_service().get_givers():
            self.giver_box.addItem(f'{name} {g_index}', id)

    def show_items(self):
        self.item_box.addItem('Выберете товар', None)
        for id, name, price in DB_service().get_items():
            self.item_box.addItem(f'{name} --- {price} руб.', id)

    # блок редактирования

    def load_order(self, order_id):
        db = DB_service()
        row = db.get_order_by_id(order_id)

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
