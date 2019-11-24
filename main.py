# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Desktop\app\mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from mw import *
from mainWindow import *
from psycopg2 import sql
import psycopg2
        
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.connect_button.clicked.connect(self.on_connect_click)
        self.render_button.clicked.connect(self.on_render_click)

    @QtCore.pyqtSlot()
    def on_connect_click(self):
        textboxValue = "1111"
        QMessageBox.question(self, 'Message', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        self.conn = psycopg2.connect(dbname=self.line_db.text(), user=self.line_user.text(), 
                        password=self.line_pwd.text(), host=self.line_host.text())
        self.line_user.setText("CONNECTED")
        self.line_pwd.setText("")
        
    @QtCore.pyqtSlot()
    def on_render_click(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM TEST;")
            self.tableWidget.setRowCount(5)
            self.tableWidget.setColumnCount(1)
            for row in cursor:
                for i in row:
                    print(i)
                print(row)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

