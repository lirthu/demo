import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtWidgets import (
    QDialog, QApplication, QPushButton, QMessageBox, QHBoxLayout,
    QWidget, QLabel, QVBoxLayout, QScrollArea
)
from PyQt6.uic import loadUi
from db_servives import DB_service


class ClickableOrderWidget(QWidget):
    """Карточка заказа, открывающая заказ по щелчку мыши."""
    def __init__(self, order_id, on_click, parent=None):
        super().__init__(parent)
        self.order_id = order_id
        self.on_click = on_click
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.on_click(self.order_id)
        super().mousePressEvent(event)


class OrderWin(QDialog):
    def __init__(self, user):
        super().__init__()
        self.user = user
        loadUi('ui\\order_win.ui', self)
        self.return_btn.clicked.connect(self.return_to_items)
        self.add_item_btn.clicked.connect(lambda: self.open_add_order_win())
        self.refresh_orders()

    def return_to_items(self):
        from catalog_win import CatalogWin
        self.win = CatalogWin(self.user)
        self.win.show()
        self.close()

    def display_orders(self, orders_list):
        # Не удаляем scrollWidget до удаления его содержимого: это безопаснее для Qt.
        old_widget = self.scrollArea.takeWidget()
        if old_widget is not None:
            old_widget.deleteLater()

        self.scrollWidget = QWidget()
        self.orders_layout = QVBoxLayout(self.scrollWidget)
        self.orders_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        for order in orders_list or []:
            order_id, status, address, date_created, date_delivered = order
            font = QFont('Times', 13)
            card = ClickableOrderWidget(order_id, self.open_add_order_win)
            card.setFixedSize(830, 210)
            card.setStyleSheet(
                'QWidget { border: 1px solid #777; background: white; }'
                'QWidget:hover { background: #f0f6ff; }'
            )
            layout = QHBoxLayout(card)
            layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

            info = QLabel(
                f'Артикул заказа: {order_id}<br>'
                f'Статус: {status}<br>'
                f'Адрес пункта выдачи: {address}<br>'
                f'Дата создания: {date_created}'
            )
            info.setFont(font)
            info.setFixedSize(490, 190)
            info.setWordWrap(True)
            info.setStyleSheet('border: none; background: transparent;')
            info.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            layout.addWidget(info)

            delivery = QLabel(f'Дата доставки:<br>{date_delivered or "не указана"}')
            delivery.setFont(font)
            delivery.setWordWrap(True)
            delivery.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            delivery.setFixedSize(220, 190)
            delivery.setStyleSheet('border: none; background: transparent;')
            delivery.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            layout.addWidget(delivery)
            self.orders_layout.addWidget(card)

        self.orders_layout.addStretch()

    def open_add_order_win(self, order_id=None):
        try:
            from add_order_win import AddOrderWin
            win = AddOrderWin(order_id)
            if win.exec() == QDialog.DialogCode.Accepted:
                # Удаление уже выполняется в диалоге. Сохраняем только при наличии результата.
                if win.result is not None:
                    db = DB_service()
                    if order_id is None:
                        db.save_order(win.result)
                    else:
                        db.update_order(order_id, win.result)
                self.refresh_orders()
        except Exception as error:
            QMessageBox.warning(self, 'Ошибка открытия окна', f'Ошибка: {error}')

    def refresh_orders(self):
        self.orders = DB_service().get_orders_info() or []
        self.display_orders(self.orders)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = OrderWin(None)
    win.show()
    sys.exit(app.exec())
