import pymysql
from PyQt6.QtWidgets import QMessageBox


class DB_service:
    def __init__(self):
        self.connectiojn = None
        try:
            self.connectiojn = pymysql.connect(host='localhost',
                                 database='shoes_shop',
                                 user='root',
                                 password='root')
        except Exception as e:
            QMessageBox.warning(None, 'Ошибка подключения к БД', f'Ошибка: {e}')

    def get_user_info(self, login, password):
        if