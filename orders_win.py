import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QApplication, QPushButton, QMessageBox, QHBoxLayout, QWidget, QLabel, QVBoxLayout, \
    QScrollArea
from PyQt6.uic import loadUi
from db_servives import DB_service

class OrderWin(QDialog):
    return_btn: QPushButton
    scrollArea: QScrollArea
    scrollWidget: QWidget
    add_item_btn: QPushButton
    def __init__(self, user):
        super().__init__()
        self.user = user
        loadUi('ui\\order_win.ui', self)
        self.return_btn.clicked.connect(self.return_to_items)
        self.add_item_btn.clicked.connect(self.open_add_order_win)

        self.orders = []
        self.orders = DB_service().get_orders_info()
        self.display_orders(self.orders)

    def return_to_items(self):
        from catalog_win import CatalogWin
        self.win = CatalogWin(self.user)
        self.win.show()
        self.close()

    def display_orders(self, orders_list):

        self.scrollWidget.deleteLater()

        self.scrollWidget = QWidget()
        self.scrollArea.setWidget(self.scrollWidget)

        self.orders_layout = QVBoxLayout()
        self.scrollWidget.setLayout(self.orders_layout)

        for orders in orders_list:
            font = QFont('Times', 13)
            order_widget = QWidget()
            order_widget.setFixedSize(850,210)
            order_layout = QHBoxLayout()
            order_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            order_widget.setLayout(order_layout)
            self.orders_layout.addWidget(order_widget)

            # print(orders)

            order_info_label = QLabel(f"Артикул: {orders[0]}<br>"
                                      f"Статус {orders[1]}<br>"
                                      f"Адрес пункта выдачи {orders[2]}<br>"
                                      f"Дата {orders[1]}<br>"
                                        )
            order_info_label.setFont(font)
            order_info_label.setFixedSize(650,200)
            order_info_label.setWordWrap(True)
            order_info_label.setStyleSheet("border: 1px solid black")
            order_layout.addWidget(order_info_label)

            order_delivery_label = QLabel(f"Дата доставки:<br>{orders[2]} <br>")
            order_delivery_label.setFont(font)
            order_delivery_label.setWordWrap(True)
            order_delivery_label.setStyleSheet("border: 1px solid black")
            order_delivery_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            order_delivery_label.setFixedSize(150,200)
            order_layout.addWidget(order_delivery_label)

    def open_add_order_win(self, order_id=None):
        try:
            from add_order_win import AddOrderWin
            from db_servives import DB_service
            win = AddOrderWin(order_id)
            win.exec()
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
    win = OrderWin(None)
    win.show()
    sys.exit(app.exec())
