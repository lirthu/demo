import pymysql
from PyQt6.QtSql import result
from PyQt6.QtWidgets import QMessageBox


class DBConnector:
    def __init__(self):
        self.conn = None
        try:
            self.conn = pymysql.connect(host='localhost',
                                 database='shoes_shop',
                                 user='root',
                                 password='root')
        except Exception as e:
            QMessageBox.warning(None, 'Ошибка подключения к БД!', f'Ошибка {e}')

    def get_user_info(self, login, password):
        if not self.conn:
            return None
        try:
            with self.conn.cursor() as c:
                c.execute('''SELECT * FROM u.user_id, u.surename, u.name, u.thirdname, u.id_role, r.name
                            FROM users u
                            JOIN roles r on u.id_role = r.role_id
                            WHERE u.login = %s and password = %s''', (str(login), str(password),))
                res = c.fetchall()
                if res:
                    return User(*result[0])
                else:
                    QMessageBox.warning(None, 'Ошибка авторизации!', 'Неверный логин или пароль!')
        except Exception as e:
            QMessageBox.warning(None, 'Ошибка получения данных', f'Ошибка {e}')
            return None
