# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Desktop\app\mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from mw import *
from queries import *
import queries
from mainWindow import *
from psycopg2 import sql
import psycopg2
from PyQt5.QtWidgets import QTableWidgetItem
import inspect


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.connect_button.clicked.connect(self.on_connect_click)
        self.render_button.clicked.connect(self.on_render_click)
        self.button_tables.clicked.connect(self.on_render_table_click)
        self.connected = False
        dc = dir(queries)
        
        try:
            dcc = inspect.getmembers(queries)
        except:
            dcc = inspect.getmembers(Queries)
        self.dcf = {}
        for c in dcc:
            if c[0][0:4] == "get_": 
                fdoc = inspect.getdoc(c[1])
                self.comboBox.addItem(c[0])
                lines = fdoc.split("\n")
                inputs_next = False
                inputs = []
                for i in range(len(lines)):
                    l = lines[i]
                    l_no_space = l.replace(" ", "")
                    if l_no_space == "Inputs:" or l_no_space == "Input:":
                        inputs_next = True
                    if l_no_space == "Outputs:" or l_no_space == "Output:":
                        inputs_next = False
                    if inputs_next:
                        try:
                            to_append = l.split(":")[1]
                            if to_append[0] == " ": 
                                to_append = to_append[1:]
                            inputs.append(to_append)
                        except:
                            pass
                self.dcf[lines[0]] = {
                    "doc": fdoc, 
                    "inputs": inputs,
                    "func": c[0],
                    "func_ptr": c[1],
                    "func_args": inspect.getfullargspec(c[1]).args
                }

        self.comboBox.clear()
        for k in self.dcf.keys():
            self.comboBox.addItem(k)
        self.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
        self.query_params = []
        for i in range(4):
            self.addInputLine()
        self.on_combobox_changed()

    def addInputLine(self):
        self.query_params.append(QtWidgets.QHBoxLayout())
        lqp = len(self.query_params)
        self.query_params[-1].setObjectName(f"hlayout_query_param_{lqp}")
        self.query_params[-1].label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.query_params[-1].label.setObjectName(f"label_query_param_{lqp}")
        self.query_params[-1].addWidget(self.query_params[-1].label)
        self.query_params[-1].line = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.query_params[-1].line.setObjectName(f"line_query_param_{lqp}")
        self.query_params[-1].addWidget(self.query_params[-1].line)
        self.query_form.addLayout(self.query_params[-1])


    @QtCore.pyqtSlot()
    def on_connect_click(self):
        try:
            if not self.connected:        
                try:
                    self.cursor.close()
                    self.conn.close()
                except:
                    pass
                self.conn = psycopg2.connect(dbname=self.line_db.text(), user=self.line_user.text(), 
                                password=self.line_pwd.text(), host=self.line_host.text())
                self.cursor = self.conn.cursor()
                self.line_user.setText("CONNECTED")
                self.line_pwd.setText("")
                self.connected = True
                self.connect_button.setText("disconnect")
                self.cursor.execute("""SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public'""")
                self.comboBox_tables.clear()
                for table in self.cursor.fetchall():
                    self.comboBox_tables.addItem(table[0])
            else:
                self.connected = False
                try:
                    self.cursor.close()
                    self.conn.close()
                except:
                    pass
                self.line_user.setText("postgres")
                self.line_pwd.setText("1")
                self.connect_button.setText("login")
                self.comboBox_tables.clear()
            self.line_user.setEnabled(not self.connected)
            self.line_pwd.setEnabled(not self.connected)
            self.line_host.setEnabled(not self.connected)
            self.line_db.setEnabled(not self.connected)
        except:
            pass

    
    def get_rc(self, cf):
            if len(cf): return len(cf[0])
            else: return 0

    @QtCore.pyqtSlot()
    def on_render_click(self):
        try:            
            cur_query = self.dcf[self.comboBox.currentText()]
            num_args = len(cur_query["func_args"])
            cf = cur_query["func_ptr"](self.cursor, *[self.query_params[i].line.text() for i in range(num_args-1)])
            if cf is None:
                cf = cursor.fetchall()

            self.render_query(cf)
        except:
            # QMessageBox.question(self, 'error", QMessageBox.Yes | QMessageBox.No)
            QMessageBox.about(self, "error", "query error")

    @QtCore.pyqtSlot()
    def on_render_table_click(self):
        try:            
            cf = select_table(self.cursor, self.comboBox_tables.currentText())
            self.render_query(cf)
        except:
            pass


    @QtCore.pyqtSlot()
    def on_combobox_changed(self):
        try:
            curtext = self.comboBox.currentText()
            cur_inputs = self.dcf[curtext]["inputs"]
            len_inputs = len(cur_inputs)
            for i in range(4):
                qp = self.query_params[i]
                if i >= len_inputs:
                    qp.label.setText("")
                    qp.line.setEnabled(False)
                    continue
                qp.line.setEnabled(True)
                if cur_inputs[i].replace(" ", "") == "началопериода":
                    qp.line.setText("2019-01-01")
                elif cur_inputs[i].replace(" ", "") == "конецпериода":
                    qp.line.setText("2019-12-31")
                else:
                    qp.line.setText("")
                qp.label.setText(cur_inputs[i])
        except:
            pass
            
    def render_query(self, cf):
        self.tableWidget.setColumnCount(self.get_rc(cf))
        self.tableWidget.setRowCount(len(cf))
        for i in range(len(cf)):
            for j in range(len(cf[0])):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(cf[i][j])))
        self.tableWidget.setHorizontalHeaderLabels([d.name for d in self.cursor.description])
    
            
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

