import pymysql
from PyQt6.QtWidgets import QMessageBox
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



