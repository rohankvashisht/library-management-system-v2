import sys
import os
import time
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QGridLayout, QSizePolicy, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery

# from PyQt6.QtGui import QGuiApplication

class MainApp (QWidget):
  def __init__(self):
    super().__init__()
    uic.loadUi('dashboard.ui', self)
    self.setWindowTitle('Institute Library Portal')

class LoginWindow (QWidget):
  def __init__(self):
    super().__init__()
    uic.loadUi('login.ui', self)
    self.setWindowTitle('App Login')

    self.button_login.clicked.connect(self.checkCredential)

    self.connectToDB()

  def connectToDB(self):
    # https://doc.qt.io/qt-6/sql-driver.html#qsqlite

    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('admin.db')

    if not db.open():
      self.label_message.setText('Connection failed')
      print('error while connecting to database...')

  def checkCredential(self):
        username = self.input_username.text()
        password = self.input_password.text()

        query = QSqlQuery()
        query.prepare('SELECT * FROM UserLogin WHERE UserID=:username')
        query.bindValue(':username', username)
        query.exec()

        if query.first():
            if query.value('Password') == password:
                time.sleep(1)
                self.mainApp = MainApp()
                self.mainApp.show()
                self.close()
            else:
                self.label_message.setText('Password is incorrect')
        else:
            self.label_message.setText('Username is not found')


if __name__ == '__main__':
  # don't auto scale when drag app to a different monitor.
  # QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

  app = QApplication(sys.argv)
  app.setStyleSheet('''

    QWidget {
      font-size: 18px;
    }
    QLineEdit {
      height: 200px;
    }

  ''')

  loginWindow = LoginWindow()
  loginWindow.show()

  try:
    sys.exit(app.exec())
  except SystemExit:
     print('Closing Window...')