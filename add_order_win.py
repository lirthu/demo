import sys

from PyQt6.QtWidgets import QDialog, QApplication, QPushButton, QMessageBox, QComboBox, QLineEdit, QSpinBox, \
    QScrollArea, QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.uic import loadUi
from db_servives import DB_service

class AddOrderWin(QDialog):
    def __init__(self, order_id=None):
        super().__init__()
        loadUi('ui\\add_order.ui', self)
        self.order_id = order_id
        self.db = DB_service()
        self.order_items = {}  # item_id -> quantity

        self.item_layout = QVBoxLayout()
        self.item_layout.setContentsMargins(4, 4, 4, 4)
        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.item_layout)
        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setWidgetResizable(True)

        self.cancel.clicked.connect(self.reject)
        self.pushButton_3.clicked.connect(self.save_order)
        self.add_btn.clicked.connect(self.add_item)
        self.show_users()
        self.show_givers()
        self.show_items()

        if self.order_id is None:
            self.delete_btn.hide()
            self.status_line.setText('Новый')
        else:
            # При редактировании состав только отображается из БД; добавление скрываем.
            self.item_box.hide()
            self.spinBox.hide()
            self.add_btn.hide()
            self.label_9.hide()
            self.load_order()
            self.delete_btn.clicked.connect(self.delete_order)

    def show_users(self):
        self.user_box.addItem('Выберите клиента', None)
        for user_id, surname, name, role in self.db.get_users() or []:
            self.user_box.addItem(f'{surname} {name}: {role}', user_id)

    def show_givers(self):
        self.giver_box.addItem('Выберите пункт выдачи', None)
        for giver_id, index, address in self.db.get_givers() or []:
            self.giver_box.addItem(f'{address} ({index})', giver_id)

    def show_items(self):
        self.item_box.addItem('Выберите товар', None)
        for item_id, name in self.db.get_items() or []:
            self.item_box.addItem(name, item_id)

    def add_item(self):
        item_id = self.item_box.currentData()
        if item_id is None:
            QMessageBox.warning(self, 'Товар не выбран', 'Выберите товар из списка.')
            return
        quantity = self.spinBox.value()
        self.order_items[item_id] = self.order_items.get(item_id, 0) + quantity
        self.render_items()

    def render_items(self):
        while self.item_layout.count():
            item = self.item_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        names = {item_id: name for item_id, name in (self.db.get_items() or [])}
        if not self.order_items:
            self.item_layout.addWidget(QLabel('Состав заказа пуст'))
        for item_id, quantity in self.order_items.items():
            row = QWidget()
            layout = QHBoxLayout(row)
            layout.addWidget(QLabel(f'{names.get(item_id, "Товар #" + str(item_id))} — {quantity} шт.'))
            if self.order_id is None:
                remove_btn = QPushButton('Убрать')
                remove_btn.clicked.connect(lambda checked=False, iid=item_id: self.remove_item(iid))
                layout.addWidget(remove_btn)
            self.item_layout.addWidget(row)
        self.item_layout.addStretch()

    def remove_item(self, item_id):
        self.order_items.pop(item_id, None)
        self.render_items()

    def save_order(self):
        if self.user_box.currentData() is None or self.giver_box.currentData() is None:
            QMessageBox.warning(self, 'Не заполнены данные', 'Выберите клиента и пункт выдачи.')
            return
        if self.order_id is None and not self.order_items:
            QMessageBox.warning(self, 'Пустой заказ', 'Добавьте хотя бы один товар в заказ.')
            return
        data = {
            'date_created': self.line_create_order.text().strip(),
            'date_delivered': self.line_deliver.text().strip() or None,
            'id_giver': self.giver_box.currentData(),
            'id_user': self.user_box.currentData(),
            'code': self.code_giver_line.text().strip(),
            'status': self.status_line.text().strip() or 'Новый',
            'items': self.order_items.copy(),
        }
        if not data['date_created']:
            QMessageBox.warning(self, 'Не заполнена дата', 'Укажите дату создания заказа.')
            return
        self.result = data
        self.accept()

    def load_order(self):
        row = self.db.get_order_by_id(self.order_id)
        if not row:
            QMessageBox.warning(self, 'Заказ не найден', 'Не удалось загрузить заказ.')
            return
        order_id, date_created, date_delivered, id_giver, id_user, code, status = row
        self.setWindowTitle(f'Редактирование заказа №{order_id}')
        self.line_create_order.setText(str(date_created or ''))
        self.line_deliver.setText(str(date_delivered or ''))
        self.code_giver_line.setText(str(code or ''))
        self.status_line.setText(str(status or ''))
        self.user_box.setCurrentIndex(max(0, self.user_box.findData(id_user)))
        self.giver_box.setCurrentIndex(max(0, self.giver_box.findData(id_giver)))
        self.order_items = self.db.get_order_items(self.order_id) or {}
        self.render_items()

    def delete_order(self):
        answer = QMessageBox.question(
            self, 'Удаление', 'Вы уверены, что хотите удалить заказ?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.db.delete_order(self.order_id)
            self.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AddOrderWin()
    win.show()
    sys.exit(app.exec())
