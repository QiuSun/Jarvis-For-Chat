# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'input_error_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Input_Error_Dialog(object):
    def setupUi(self, Input_Error_Dialog):
        Input_Error_Dialog.setObjectName("Input_Error_Dialog")
        Input_Error_Dialog.resize(185, 137)
        self.label = QtWidgets.QLabel(Input_Error_Dialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 161, 71))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Input_Error_Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 100, 75, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Input_Error_Dialog)
        self.pushButton.clicked.connect(Input_Error_Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Input_Error_Dialog)

    def retranslateUi(self, Input_Error_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Input_Error_Dialog.setWindowTitle(_translate("Input_Error_Dialog", "输入格式错误"))
        self.label.setText(_translate("Input_Error_Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#000000;\">输入格式错误</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ff0000;\">#号只能为0个或2个</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#000000;\">请重新编辑您的群发模板</span></p></body></html>"))
        self.pushButton.setText(_translate("Input_Error_Dialog", "确定"))

