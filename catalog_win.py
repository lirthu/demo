import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QApplication, QPushButton, QLabel, QWidget, QScrollArea, QVBoxLayout, QHBoxLayout, \
    QComboBox, QLineEdit, QMessageBox
from PyQt6.uic import loadUi
from db_servives import DB_service

class CatalogWin(QDialog):

    exit_btn: QPushButton
    name_label: QLabel
    scrollWidget: QWidget
    scrollArea: QScrollArea
    sort_box: QComboBox
    filter_box: QComboBox
    search_line: QLineEdit
    search_label: QLabel
    add_item_btn: QPushButton
    open_orders_btn: QPushButton

    def __init__(self, user=None):
        try:
            super().__init__()
            loadUi('ui\\catalog_win.ui',self)
            self.user = user

            self.is_admin = user is not None and user.id_role == 1
            is_manager_or_admin = user is not None and user.id_role in (1, 2)

            self.products_list = []
            self.filtered_products = []

            try:
                if self.user:
                    self.name_label.setText(f'{self.user.surename} {self.user.name} {self.user.thirdname}')
            except Exception as err:
                print(err)

            # Блок фильтров и сортировки
            for sid, sname in DB_service().get_dealers():
                self.filter_box.addItem(sname, sname)

            self.sort_box.addItem('Количество ↑', 'asc')
            self.sort_box.addItem('Количество ↓', 'desc')

            self.sort_box.setVisible(is_manager_or_admin)
            self.filter_box.setVisible(is_manager_or_admin)
            self.search_line.setVisible(is_manager_or_admin)
            self.search_label.setVisible(is_manager_or_admin)
            self.add_item_btn.setVisible(self.is_admin)
            self.open_orders_btn.setVisible(self.is_admin)

            # привязка поиска фильтров сортировки
            self.search_line.textChanged.connect(self.apply_filters)
            self.sort_box.currentIndexChanged.connect(self.apply_filters)
            self.filter_box.currentIndexChanged.connect(self.apply_filters)

            self.add_item_btn.clicked.connect(lambda: self.open_item_dialog(None))
            self.exit_btn.clicked.connect(self.open_auth_win)
            self.open_orders_btn.clicked.connect(self.open_orders)

            self.refresh_products()
        except Exception as error:
            QMessageBox.warning(self, 'Error', f'Erorr: {error}')

    def refresh_products(self):
        self.products_list = DB_service().get_products_info() or []
        self.apply_filters()

    def apply_filters(self):
        try:
            search_query  = self.search_line.text().lower()
            filter_box = self.filter_box.currentData()
            sort_box = self.sort_box.currentData()

            result = []

            for p in self.products_list:
                if search_query:
                    haystack = (
                        f"{p.name} {p.category} {p.id_dealer}"
                    ).lower()
                    if search_query not in haystack:
                        continue

                if filter_box is not None and p.id_dealer != filter_box:
                    continue

                result.append(p)

            if sort_box == 'asc':
                result.sort(key=lambda p: p.amount)
            elif sort_box == 'desc':
                result.sort(key=lambda p: p.amount, reverse=True)

            self.filtered_products = result
            self.display_products(result)
        except Exception as error:
            QMessageBox.warning(self, 'Error', f'Erorr: {error}')

    def display_products(self, products_list):

        self.scrollWidget.deleteLater()

        self.scrollWidget = QWidget()
        self.scrollArea.setWidget(self.scrollWidget)

        self.products_layout = QVBoxLayout()
        self.scrollWidget.setLayout(self.products_layout)

        for product in products_list:
            font = QFont('Times', 13)
            product_widget = QWidget()
            product_widget.setFixedSize(810,210)
            product_layout = QHBoxLayout()
            product_widget.setLayout(product_layout)
            self.products_layout.addWidget(product_widget)

            if product.discount > 15:
                product_widget.setStyleSheet("""background-color: #2E8B57""")

            if product.amount == 0:
                product_widget.setStyleSheet("""background-color: #89ffee""")

            if product.discount > 0:
                price = float(product.price)
                discounted_price = round(price * (1 - product.discount / 100), 2)
                price_text = f"<s style='color:red'>{product.price}</s> {discounted_price}"
            else:
                price_text = str(product.price)

            product_photo_label = QLabel()
            product_photo_label.setFixedSize(200, 200)
            product_photo_label.setStyleSheet("border: 1px solid black")
            photo = product.photo.scaled(product_photo_label.size())
            product_photo_label.setPixmap(photo)
            product_layout.addWidget(product_photo_label)
            product_info_label = QLabel(f"{product.category} | {product.name}<br>"
                                        f"Описание товара {product.description} <br>"
                                        f"Производитель {product.id_creator} <br>"
                                        f"Поставщик {product.id_dealer} <br>"
                                        f"Цена {price_text} <br>"
                                        f"Единица измерения {product.shtuki} <br>"
                                        f"Кол-во на складе {product.amount} <br>")
            product_info_label.setFont(font)
            product_info_label.setFixedSize(300,200)
            product_info_label.setWordWrap(True)
            product_info_label.setStyleSheet("border: 1px solid black")
            product_layout.addWidget(product_info_label)

            product_discount_label = QLabel(f"Действующая скидка:<br>{product.discount}% <br>")
            product_discount_label.setFont(font)
            product_discount_label.setWordWrap(True)
            product_discount_label.setStyleSheet("border: 1px solid black")
            product_discount_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            product_discount_label.setFixedSize(200,200)
            product_layout.addWidget(product_discount_label)
            if self.is_admin:
                product_widget.setCursor(Qt.CursorShape.PointingHandCursor)
                product_widget.mouseDoubleClickEvent = (
                    lambda event, pid=product.item_id: self.open_item_dialog(pid)
                )

    def open_item_dialog(self, item_id=None):
        try:
            from add_item_win import AddItemWindow
            win = AddItemWindow(self, item_id=item_id)
            if win.exec() == QDialog.DialogCode.Accepted:
                db = DB_service()
                if item_id is None:
                    db.save_product(*win.result)
                else:
                    db.update_product(*win.result)
                self.refresh_products()
        except Exception as error:
            print(error)

    def open_auth_win(self):
        from auth_win import AuthWin
        self.win = AuthWin()
        self.win.show()
        self.close()

    def open_orders(self):
        try:
            from orders_win import OrderWin
            self.win = OrderWin(self.user)
            self.win.show()
            self.close()
        except Exception as error:
            QMessageBox.warning(self, 'Ошибка', f'Ошибка {error}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = CatalogWin()
    win.show()
    sys.exit(app.exec())
