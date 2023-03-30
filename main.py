import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout
from PyQt6.QtGui import QIcon

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Institute Library Portal')
        self.setWindowIcon(QIcon('favicon.ico'))
        self.resize(500, 350) # width, height

        layout = QVBoxLayout()
        self.setLayout(layout)

        # widgets
        self.inputField = QLineEdit()
        button = QPushButton()
        self.output = QTextEdit()

        layout.addWidget(self.inputField)
        layout.addWidget(button)
        layout.addWidget(self.output)


# app = QApplication([])
app = QApplication(sys.argv)

window = MyApp()
window.show()

sys.exit(app.exec())