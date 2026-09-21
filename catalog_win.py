import sys

from PyQt6.QtWidgets import QDialog, QApplication, QPushButton, QLabel, QWidget, QScrollArea, QVBoxLayout
from PyQt6.uic import loadUi
from product import Product as product
from db_servives import DB_service


class CatalogWin(QDialog):

    exit_btn: QPushButton
    name_label: QLabel
    scrollWidget: QWidget
    scrollArea: QScrollArea

    def __init__(self, user=None):
        super().__init__()
        loadUi('ui\\catalog_win.ui',self)
        self.exit_btn.clicked.connect(self.exit_app)
        self.user = user

        self.products_list = DB_service.get_product_info()

        if self.products_list:
            self.display_products(self.products_list)

        if self.user:
            self.name_label.setText(f'{self.user.surename} {self.user.name} {self.user.thirdname}')

        self.exit_btn.clicked.connect(self.open_auth_win)

    def display_products(self, products_list):
        self.scrollWidget.deleteLater()

        self.scrollWidget = QWidget()
        self.scrollArea.setWidget(self.scrollWidget)

        self.products_layout = QVBoxLayout()
        self.scrollWidget.setLayout(self.products_layout)

        for products in products_list:
            product_widget = QWidget()
            product_layout = QVBoxLayout()
            product_widget.setLayout(product_layout)
            self.products_layout.addWidget(product_widget)

            if product.discount > 15:
                product_widget.setStyleSheet("""background-color: #2E8B57""")

            if product.amount == 0:
                product_widget.setStyleSheet("""background-color: aqua""")

            if product.discount > 0:
                discounted_price = round(product.price * (1 - product.discount / 100), 2)
                price_text = f"<s style='color:red'>{product.price}<s> {discounted_price}"
            else:
                price_text = str(product.price)

            product_photo_label = QLabel()
            product_photo_label.setFixedSize(200, 200)
            product_photo_label.setStyleSheet("border: 1px solid black")
            photo = product.photo.scaled(product_photo_label.size())
            product_photo_label.setPixmap(photo)
            product_layout.addWidget(product_photo_label)
            product_info_label = QLabel(f"{product.name}<br>"
                                        f"Описание товара {} <br>"
                                        f"Производитель {} <br>"
                                        f"Поставщик {} <br>"
                                        f"Цена {} <br>"
                                        f"Единица измерения {} <br>"
                                        f"Кол-во на складе {} <br>")




    def open_auth_win(self):
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = CatalogWin()
    win.show()
    sys.exit(app.exec())
