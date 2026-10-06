import pymysql
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QMessageBox

from product import Product
from user import User

class DB_service:
    def __init__(self):
        self.connection = None
        try:
            self.connection = pymysql.connect(host='localhost',
                                 database='shoes_shop',
                                 user='root',
                                 password='root')
        except Exception as e:
            QMessageBox.warning(None, 'Ошибка подключения к БД', f'Ошибка: {e}')

    def get_user_info(self, login, password):
        if not self.connection:
            return None
        try:
            with self.connection.cursor() as c:
                c.execute('''SELECT u.user_id, u.surename, u.name, u.thirdname, u.id_role, r.name
                            FROM users u
                            JOIN roles r on r.role_id = u.id_role
                            WHERE login = %s and password = %s''', (login, password,))
                res = c.fetchall()
                if res:
                    return User(*res[0])
                else:
                    QMessageBox.warning(None, 'Ошибка авторизации!', 'Неверный логин или пароль')
                    return None
        except Exception as e:
            QMessageBox.warning(None, 'Ошибка получения данных!', f'Ошибка: {e}')
            return None

    def get_product_info(self):
        if not self.connection:
            return None
        try:
            with self.connection.cursor() as c:
                c.execute('''select i.item_id, i.name, i.price, i.category, i.description, i.discount,
                i.amount, c.name, d.name, i.shtuki, i.photo
                FROM items i
                JOIN creators c on c.creator_id = i.id_creator
                JOIN dealers d on d.dealer_id = i.id_dealer''')
                res = c.fetchall()
                products_list = []
                if res:
                    for product in res:
                        if product[10]:
                            photo_img = QImage(product[10])
                        else:
                            photo_img = QImage('photos/picture.png')
                        photo_pixmap = QPixmap.fromImage(photo_img)

                        products_list.append(Product(*product[:10], photo_pixmap))
                    return products_list
                else:
                    QMessageBox.warning(None, 'Ошибка получения данных', 'Товары не найдены')
                    return None
        except Exception as e:
            QMessageBox.warning(None, 'Ошибка получения данных', f'Ошибка: {e}')
            return None
