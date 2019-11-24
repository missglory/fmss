from PyQt5.QtWidgets import QAction, QApplication, QDesktopWidget, QFormLayout, QGroupBox, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Icon')
        # self.setWindowIcon(QIcon('web.png'))

        self.show()



class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Login'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 140
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
    
        self.loginFormGroupBox = QGroupBox("Form layout")
        layout = QFormLayout()
        layout.addRow(QLabel("User:"), QLineEdit("postgres"))
        layout.addRow(QLabel("Password:"), QLineEdit("1"))
        layout.addRow(QLabel("Database:"), QLineEdit("postgres"))
        self.loginFormGroupBox.setLayout(layout)

        self.connect_button = QPushButton('Connect', self)
        layout.addRow((self.connect_button))
        self.setLayout(layout)
        self.connect_button.move(20,80)
        self.connect_button.clicked.connect(self.on_connect_click)
        # self.center()
        self.show()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    @pyqtSlot()
    def on_connect_click(self):
        textboxValue = " 123123 "
        QMessageBox.question(self, 'Message', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("")

    @pyqtSlot()
    def on_click(self):
        textboxValue = self.textbox.text()
        QMessageBox.question(self, 'Message', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("")
