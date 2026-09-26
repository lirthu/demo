import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QApplication, QPushButton, QLabel, QWidget, QScrollArea, QVBoxLayout, QHBoxLayout
from PyQt6.uic import loadUi
from db_servives import DB_service

class CatalogWin(QDialog):

    exit_btn: QPushButton
    name_label: QLabel
    scrollWidget: QWidget
    scrollArea: QScrollArea

    # def set_font(self):
    #     self.font = QtGui.QFont()
    #     self.font.setFamily("TimesNewRoman")
    #     self.font.setPointSize(13)

    def __init__(self, user=None):
        super().__init__()
        loadUi('ui\\catalog_win.ui',self)
        self.user = user

        # self.set_font()

        self.products_list = DB_service().get_product_info()

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

        for product in products_list:
            product_widget = QWidget()
            product_layout = QHBoxLayout()
            product_widget.setLayout(product_layout)
            self.products_layout.addWidget(product_widget)

            if product.discount > 15:
                product_widget.setStyleSheet("""background-color: #2E8B57""")

            if product.amount == 0:
                product_widget.setStyleSheet("""background-color: #89ffee""")

            if product.discount > 0:
                discounted_price = round(product.price * (1 - product.discount / 100), 2)
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
                                        f"Поставщик {product.id_dealer}"
                                        f"Цена {price_text} <br>"
                                        f"Единица измерения {product.shtuki} <br>"
                                        f"Кол-во на складе {product.amount} <br>")

            product_info_label.setFixedSize(300,200)
            # product_info_label.setFont(self.font)
            product_info_label.setWordWrap(True)
            product_info_label.setStyleSheet("border: 1px solid black")
            product_layout.addWidget(product_info_label)

            product_discount_label = QLabel(f"Действующая скидка:<br>{product.discount}% <br>")
            # product_discount_label.setFont(self.font)
            product_discount_label.setWordWrap(True)
            product_discount_label.setStyleSheet("border: 1px solid black")
            product_discount_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            product_layout.addWidget(product_discount_label)

    def open_auth_win(self):
        from auth_win import AuthWin
        self.win = AuthWin()
        self.win.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = CatalogWin()
    win.show()
    sys.exit(app.exec())
