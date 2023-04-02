import sys
import os
import time
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QGridLayout, QSizePolicy, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6 import uic
from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery

# from PyQt6.QtGui import QGuiApplication

class MainApp (QWidget):
  def __init__(self):
    super().__init__()
    uic.loadUi('dashboard.ui', self)
    self.setWindowTitle('Institute Library Portal')
    self.setWindowIcon(QIcon('favicon.ico'))

    self.button_logout.clicked.connect(self.logout)
    self.button_add_books.clicked.connect(self.addBooks)
    self.button_issue_books.clicked.connect(self.issueBooks)
    self.button_edit_books.clicked.connect(self.editBooks)
    self.button_return_books.clicked.connect(self.returnBooks)
    self.button_delete_books.clicked.connect(self.deleteBooks)
    self.button_search_books.clicked.connect(self.searchBooks)
    self.button_show_books.clicked.connect(self.showBooks)

  def connectToDB(self, db_name):
    # https://doc.qt.io/qt-6/sql-driver.html#qsqlite

    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(db_name)

    if not db.open():
      self.label_dashboard_message.setText('Connection failed')
      print('Error while connecting to database: ', db_name)
  
  def logout(self):
    # code
    loginWindow.show()
    loginWindow.input_password.setText('')
    self.close()

  def addBooks(self):
    self.add_books_object = AddBooks()
    self.add_books_object.show()
    self.close()

  def issueBooks(self):
    self.issue_books_object = IssueBooks()
    self.issue_books_object.show()
    self.close()

  def editBooks(self):
    # code
    pass

  def returnBooks(self):
    # code
    pass

  def deleteBooks(self):
    # code
    pass

  def searchBooks(self):
    # code
    pass

  def showBooks(self):
    self.show_books_object = ShowBooks()
    self.show_books_object.show()


class LoginWindow (QWidget):
  def __init__(self):
    super().__init__()
    uic.loadUi('login.ui', self)
    self.setWindowTitle('App Login')

    self.button_login.clicked.connect(self.checkLoginCredential)

    self.connectToDB('admin.db')

  def connectToDB(self, db_name):
    # https://doc.qt.io/qt-6/sql-driver.html#qsqlite

    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(db_name)

    if not db.open():
      self.label_login_message.setText('Connection failed')
      print('Error while connecting to database: ', db_name)

  def checkLoginCredential(self):
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
                self.label_login_message.setText('Password is incorrect')
        else:
            self.label_login_message.setText('Username is not found')

class ShowBooks (QWidget):
  def __init__(self):
    super().__init__()

    self.window_width, self.window_height = 300, 300
    self.resize(self.window_width, self.window_height)
    self.setWindowTitle('Book View')

    layout = QVBoxLayout()
    self.setLayout(layout)

    labels = {}
    labels['Book Name'] = QLabel('Book Name')
    
    self.connectToDB('StoreBooks.db')

    query = QSqlQuery()
    query.prepare('SELECT * FROM Books')
    query.exec()
  
    if query.first():
      rec = query.record()
      print('Number of columns: ', rec.count()-1)

      query.previous()

      list_of_books = []

      while query.next():
        list_of_books.append(query.value('Title'))

      for book in list_of_books:
        labels[book] = QLabel(book)
  
      for _, item in labels.items():
        layout.addWidget(item)

    else:
      self.label_dashboard_message.setText('No Books found!')

  def connectToDB(self, db_name):
    # https://doc.qt.io/qt-6/sql-driver.html#qsqlite

    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(db_name)

    if not db.open():
      self.label_dashboard_message.setText('Connection failed')
      print('Error while connecting to database: ', db_name)

class AddBooks (QWidget):
  def __init__(self):
    super().__init__()
    uic.loadUi('add_books.ui', self)
    self.setWindowTitle('Add Books')

    book_id = self.input_book_id.text()
    book_title = self.input_book_title.text()
    book_author = self.input_book_author.text()
    book_edition = self.input_book_edition.text()
    book_price = self.input_book_price.text()

    self.button_submit_book.clicked.connect(self.submitNewBook)

    self.button_back.clicked.connect(self.revertToMainWindow)

  def connectToDB(self, db_name):
    # https://doc.qt.io/qt-6/sql-driver.html#qsqlite

    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(db_name)

    if not db.open():
      self.label_login_message.setText('Connection failed')
      print('Error while connecting to database: ', db_name)
  
  def submitNewBook(self):
    self.connectToDB('StoreBooks.db')

    query = QSqlQuery()
    query.prepare(
      f"""INSERT INTO Books (BookID, Title, Author, Edition, Price) VALUES ('{self.input_book_id.text()}','{self.input_book_title.text()}','{self.input_book_author.text()}','{self.input_book_edition.text()}', '{self.input_book_price.text()}')"""
    )
    query.exec()

    if query.first():
      print('Book added successfully')
      self.input_book_id.setText('')
      self.input_book_title.setText('')
      self.input_book_author.setText('')
      self.input_book_edition.setText('')
      self.input_book_price.setText('')
    else:
      print('Unable to add book')


  def revertToMainWindow(self):
    self.mainApp = MainApp()
    self.mainApp.show()
    self.close()

class IssueBooks (QWidget):
  def __init__(self):
    super().__init__()
    uic.loadUi('issue_books.ui', self)
    self.setWindowTitle('Issue Books')

    book_id = self.input_book_id.text()
    student_id = self.input_student_id.text()
    return_date = self.input_return_date.text()

    self.button_issue_book.clicked.connect(self.issueBook)

    self.button_back.clicked.connect(self.revertToMainWindow)

  def connectToDB(self, db_name):
    # https://doc.qt.io/qt-6/sql-driver.html#qsqlite

    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(db_name)

    if not db.open():
      self.label_login_message.setText('Connection failed')
      print('Error while connecting to database: ', db_name)
  
  def issueBook(self):
    self.connectToDB('StoreBooks.db')

    query = QSqlQuery()
    query.prepare(
      f"""INSERT INTO Books (BookID, Title, Author, Edition, Price) VALUES ('{self.input_book_id.text()}','{self.input_book_title.text()}','{self.input_book_author.text()}','{self.input_book_edition.text()}', '{self.input_book_price.text()}')"""
    )
    query.exec()

    if query.first():
      print('Book added successfully')
      self.input_book_id.setText('')
      self.input_book_title.setText('')
      self.input_book_author.setText('')
      self.input_book_edition.setText('')
      self.input_book_price.setText('')
    else:
      print('Unable to add book')


  def revertToMainWindow(self):
    self.mainApp = MainApp()
    self.mainApp.show()
    self.close()

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