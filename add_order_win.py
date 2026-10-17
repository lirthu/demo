import sys

from PyQt6.QtWidgets import QDialog, QApplication, QPushButton, QMessageBox, QComboBox, QLineEdit, QSpinBox, \
    QScrollArea, QWidget
from PyQt6.uic import loadUi
from db_servives import DB_service

class AddOrderWin(QDialog):
    return_btn: QPushButton
    delete_btn: QPushButton
    cancel: QPushButton
    add_btn: QPushButton

    user_box: QComboBox
    giver_box: QComboBox
    item_box: QComboBox

    line_id_order: QLineEdit
    line_create_order: QLineEdit
    line_deliver: QLineEdit
    code_giver: QLineEdit
    status_code: QLineEdit

    spin_box: QSpinBox

    scrollArea: QScrollArea
    scrollWidget: QWidget

    def __init__(self, order_id = None):
        super().__init__()
        loadUi('ui\\add_order.ui', self)
        self.order_id = order_id
        if self.order_id is None:
            self.delete_btn.hide()
        else:
            self.delete_btn.clicked.connect(self.delete_order)
        if self.order_id is not None:
            self.load_order()

        self.result = None

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

    def save_order(self):
        try:
            self.result = (
                self.line_id_order.text(),
                self.line_create_order.text(),
                self.line_deliver.text(),
                self.giver_box.currentData(),
                self.user_box.currentData(),
                self.code_giver.text(),
                self.item_box.currentData(),
                self.spin_box.value()
            )
            self.accept()
        except Exception as error:
            print(error)

    # блок редактирования

    def load_order(self):
        row = DB_service().get_order_by_id(self.order_id)
        if not row:
            return
        (line_id_order, line_create_order, line_deliver, id_giver, id_user,
         code_giver, id_item, spin_box) = row

        self.line_id_order.setText(str(line_id_order)),
        self.line_id_order.setEnabled(False),
        self.line_create_order.setText(line_create_order),
        self.line_deliver.setText(line_deliver),
        self.code_giver.setText(code_giver),

        idx = self.user_box.findData(id_user)
        if idx >= 0:
            self.user_box.setCurrentIndex(idx)
        idx = self.giver_box.findData(id_giver)
        if idx >= 0:
            self.giver_box.setCurrentIndex(idx)
        idx = self.item_box.findData(id_item)
        if idx >= 0:
            self.item_box.setCurrentIndex(idx)

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
