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

    def get_users(self):
        if not self.connection:
            return None
        try:
            with self.connection.cursor() as c:
                c.execute('''select u.user_id, u.surename, u.thirdname, r.name
                FROM users
                JOIN roles r on u.id_role = r.role_id''')
                res = c.fetchall()
                if res:
                    return res
                else:
                    QMessageBox.warning(None, 'Ошибка получения данных', 'Клиенты не найдены')
                    return None
        except Exception as e:
            QMessageBox.warning(None, 'Ошибка получения данных', f'Ошибка: {e}')
            return None

    def get_givers(self):
        if not self.connection:
            return None
        try:
            with self.connection.cursor() as c:
                c.execute('''select giver_id, index, address
                FROM give_order''')
                res = c.fetchall()
                if res:
                    return res
                else:
                    QMessageBox.warning(None, 'Ошибка получения данных', 'Пункты выдачи не найдены')
                    return None
        except Exception as e:
            QMessageBox.warning(None, 'Ошибка получения данных', f'Ошибка: {e}')
            return None

    def get_items(self):
        if not self.connection:
            return None
        try:
            with self.connection.cursor() as c:
                c.execute('''select item_id, name, price
                FROM users''')
                res = c.fetchall()
                if res:
                    return res
                else:
                    QMessageBox.warning(None, 'Ошибка получения данных', 'Товары не найдены')
                    return None
        except Exception as e:
            QMessageBox.warning(None, 'Ошибка получения данных', f'Ошибка: {e}')
            return None

    def get_products_info(self):
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

    def get_dealers(self):
        if not self.connection:
            return None
        try:
            with self.connection.cursor() as c:
                c.execute('''select d.dealer_id, d.name 
                FROM dealers d''')
                res = c.fetchall()
                if res:
                    return res
                else:
                    QMessageBox.warning(None, 'Ошибка получения данных', 'Поставщики не найдены')
                    return None
        except Exception as e:
            QMessageBox.warning(None, 'Ошибка получения данных', f'Ошибка: {e}')
            return None

    def get_creators(self):
        if not self.connection:
            return None
        try:
            with self.connection.cursor() as c:
                c.execute('''select c.creator_id, c.name 
                FROM creators c''')
                res = c.fetchall()
                if res:
                    return res
                else:
                    QMessageBox.warning(None, 'Ошибка получения данных', 'Поставщики не найдены')
                    return None
        except Exception as e:
            QMessageBox.warning(None, 'Ошибка получения данных', f'Ошибка: {e}')
            return None

    def save_product(self, id, name, description, price, category, discount, amount, photo, idcreator, iddealer, shtuki):
        if not self.connection:
            return None
        try:
            with self.connection.cursor() as c:

                c.execute('''INSERT INTO items (item_id, name, price, category, description, photo, discount,
                amount, id_creator, id_dealer, shtuki) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (id, name, price, category, description, photo, discount,
                amount, idcreator, iddealer, shtuki,))
            self.connection.commit()
        except Exception as error:
            import traceback  # ← добавить
            traceback.print_exc()
            QMessageBox.warning(None, 'Ошибка добавления товара', f'Ошибка: {error}')

    def update_product(self, id, name, description, price, category, discount,
                       amount, photo, idcreator, iddealer, shtuki):
        if not self.connection:
            return
        try:
            with self.connection.cursor() as c:
                c.execute('''UPDATE items
                             SET name=%s, price=%s, category=%s, description=%s,
                                 photo=%s, discount=%s, amount=%s,
                                 id_creator=%s, id_dealer=%s, shtuki=%s
                             WHERE item_id=%s''',
                          (name, price, category, description, photo, discount,
                           amount, idcreator, iddealer, shtuki, id))
            self.connection.commit()
        except Exception as error:
            QMessageBox.warning(None, 'Ошибка обновления товара', f'Ошибка: {error}')

    def get_product_by_id(self, item_id):
        if not self.connection:
            return None
        try:
            with self.connection.cursor() as c:
                c.execute('''SELECT item_id, name, price, category, description, discount,
                                    amount, id_creator, id_dealer, shtuki, photo
                             FROM items WHERE item_id=%s''', (item_id,))
                return c.fetchone()
        except Exception as e:
            QMessageBox.warning(None, 'Ошибка получения товара', f'Ошибка: {e}')
            return None

    def delete_product(self, item_id):
        if not self.connection:
            return
        try:
            with self.connection.cursor() as c:
                c.execute('DELETE FROM items WHERE item_id=%s', (item_id,))
            self.connection.commit()
        except Exception as error:
            QMessageBox.warning(None, 'Ошибка удаления товара', f'Ошибка: {error}')

    def get_orders_info(self):
        if not self.connection:
            return None
        try:
            with self.connection.cursor() as c:
                c.execute('''SELECT * FROM orders''')
                return c.fetchall()
        except Exception as error:
            QMessageBox.warning(None, 'Ошибка получения данных о заказах', f'Ошибка: {error}')

    def save_order(self, order_id):
        if not self.connection:
            return None
        try:
            with self.connection.cursor() as c:

                c.execute('''INSERT INTO orders (order_id) VALUES (%s)''', (order_id,))
            self.connection.commit()
        except Exception as error:
            QMessageBox.warning(None, 'Ошибка добавления товара', f'Ошибка: {error}')

    def update_order(self, order_id):
        if not self.connection:
            return
        try:
            with self.connection.cursor() as c:
                c.execute('''UPDATE orders
                             SET 
                             WHERE order_id=%s''',
                          (order_id,))
                c.execute('''UPDATE inorders
                            SET 
                            WHERE order_id=%s''',
                          (order_id,))
            self.connection.commit()
        except Exception as error:
            QMessageBox.warning(None, 'Ошибка обновления заказа', f'Ошибка: {error}')

    def delete_order(self, order_id):
        if not self.connection:
            return
        try:
            with self.connection.cursor() as c:
                c.execute('DELETE FROM inorders WHERE id_order=%s', (order_id,))
                c.execute('DELETE FROM orders WHERE order_id=%s', (order_id,))
            self.connection.commit()
        except Exception as error:
            QMessageBox.warning(None, 'Ошибка удаления товара', f'Ошибка: {error}')
        return None

    def get_order_by_id(self, order_id):
        if not self.connection:
            return None
        try:
            with self.connection.cursor() as c:
                c.execute('''SELECT order_id
                             FROM orders WHERE order_id=%s''', (order_id,))

                return c.fetchone()
        except Exception as e:
            QMessageBox.warning(None, 'Ошибка получения заказа', f'Ошибка: {e}')
            return None



if __name__ == '__main__':
    a = DB_service()
    print(a.get_dealers())