# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'keyword.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Keyword_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(820, 650)
        Form.setMinimumSize(QtCore.QSize(540, 650))
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(9, 0, 9, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setMinimumSize(QtCore.QSize(50, 0))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.LE_edit = QtWidgets.QLineEdit(self.widget)
        self.LE_edit.setMinimumSize(QtCore.QSize(274, 0))
        self.LE_edit.setObjectName("LE_edit")
        self.horizontalLayout_2.addWidget(self.LE_edit)
        self.PB_add = QtWidgets.QPushButton(self.widget)
        self.PB_add.setMinimumSize(QtCore.QSize(70, 0))
        self.PB_add.setObjectName("PB_add")
        self.horizontalLayout_2.addWidget(self.PB_add)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setMinimumSize(QtCore.QSize(50, 0))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.SA_keyword = QtWidgets.QScrollArea(self.widget)
        self.SA_keyword.setWidgetResizable(True)
        self.SA_keyword.setObjectName("SA_keyword")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 800, 597))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.SA_keyword.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.SA_keyword)
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.PB_add.setText(_translate("Form", "添加"))

