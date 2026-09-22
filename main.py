import sys

from PyQt6.QtWidgets import QApplication

from auth_win import AuthWin

app = QApplication(sys.argv)
win = AuthWin()
win.show()
sys.exit(app.exec())
