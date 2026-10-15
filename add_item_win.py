import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QDialog, QComboBox, QPushButton, QLineEdit, QLabel, QMessageBox
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets, QtGui, QtCore

from db_servives import DB_service


class AddItemWindow(QDialog):
    lid: QLineEdit
    lname: QLineEdit
    ldescription: QLineEdit
    lprice: QLineEdit
    lcategory: QLineEdit
    ldiscount: QLineEdit
    lamount: QLineEdit
    lshtuki: QLineEdit
    lphoto: QLineEdit

    dealer_box: QComboBox
    creator_box: QComboBox

    photo_label: QLabel

    browse_btn: QPushButton
    delete_btn: QPushButton
    save_btn: QPushButton
    cancel_btn: QPushButton
    def __init__(self, parent=None, item_id = None):
        super().__init__(parent)
        loadUi('ui\\add_item.ui', self)

        self.item_id = item_id

        #заполнение комбобоксов
        self.show_dealers()
        self.show_creators()

        # сбор данных с лайнэдитов
        self.result = None
        self.save_btn.clicked.connect(self.save_item)

        self.browse_btn.clicked.connect(self.browse_image)
        self.cancel_btn.clicked.connect(self.reject)
        if self.item_id is None:
            self.delete_btn.hide()
        else:
            self.delete_btn.clicked.connect(self.delete_item)

        if self.item_id is not None:
            self.load_item()

    def load_item(self):
        row = DB_service().get_product_by_id(self.item_id)
        if not row:
            return
        (iid, name, price, category, description, discount,
         amount, id_creator, id_dealer, shtuki, photo) = row

        self.lid.setText(str(iid))
        self.lid.setEnabled(False)
        self.lname.setText(name or '')
        self.lprice.setText(str(price) if price is not None else '')
        self.lcategory.setText(category or '')
        self.ldescription.setText(description or '')
        self.ldiscount.setText(str(discount) if discount is not None else '0')
        self.lamount.setText(str(amount) if amount is not None else '0')
        self.lshtuki.setText(shtuki or '')
        self.lphoto.setText(photo or '')

        idx = self.dealer_box.findData(id_dealer)
        if idx >= 0:
            self.dealer_box.setCurrentIndex(idx)
        idx = self.creator_box.findData(id_creator)
        if idx >= 0:
            self.creator_box.setCurrentIndex(idx)

        if photo:
            self.show_image_preview(photo)

    def show_dealers(self):
        self.dealer_box.addItem('Выберете поставщика')
        for sid, sname in DB_service().get_dealers():
            self.dealer_box.addItem(sname, sid)

    def show_creators(self):
        self.creator_box.addItem('Выберете Производителя')
        for sid, sname in DB_service().get_creators():
            self.creator_box.addItem(sname, sid)

    def hide_delete_btn(self):
        self.delete_btn.hide()
        return None

    def browse_image(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Выберите изображение товара",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_name:
            self.lphoto.setText(file_name)
            self.show_image_preview(file_name)

    def show_image_preview(self, image_path):
        try:
            pixmap = QPixmap(image_path)
            image = pixmap.scaled(300, 200)
            if not image.isNull():
                self.photo_label.setPixmap(image)
            else:
                self.photo_label.setText("Неверный формат\nизображения")
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            self.photo_label.setText("Ошибка\nзагрузки")

    def delete_item(self, item_id):
        if self.item_id is None:
            return
        answer = QMessageBox.question(
            self, 'Удаление',
            'Вы уверены, что хотите удалить товар?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if answer == QMessageBox.StandardButton.Yes:
            DB_service().delete_product(self.item_id)
            self.reject()

    def save_item(self):
        try:
            self.result = (
                self.lid.text(),
                self.lname.text(),
                self.ldescription.text(),
                self.lprice.text(),
                self.lcategory.text(),
                self.ldiscount.text(),
                self.lamount.text(),
                self.lphoto.text(),
                self.creator_box.currentData(),
                self.dealer_box.currentData(),
                self.lshtuki.text()
            )
            self.accept()
        except Exception as error:
            print(error)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AddItemWindow()
    win.show()
    a = AddItemWindow()
    a.show_dealers()
    sys.exit(app.exec())