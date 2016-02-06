# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create_user.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(258, 331)
        Dialog.setStyleSheet("#Dialog {\n"
"background-color: qlineargradient(spread:pad, x1:0.964, y1:0.994318, x2:1, y2:0, stop:0 rgb(19, 80, 88), stop:1 rgb(241, 242, 181));\n"
"}")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.newUser = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.newUser.sizePolicy().hasHeightForWidth())
        self.newUser.setSizePolicy(sizePolicy)
        self.newUser.setInputMask("")
        self.newUser.setText("")
        self.newUser.setAlignment(QtCore.Qt.AlignCenter)
        self.newUser.setObjectName("newUser")
        self.verticalLayout_2.addWidget(self.newUser, 0, QtCore.Qt.AlignHCenter)
        self.newPassword = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.newPassword.sizePolicy().hasHeightForWidth())
        self.newPassword.setSizePolicy(sizePolicy)
        self.newPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.newPassword.setAlignment(QtCore.Qt.AlignCenter)
        self.newPassword.setObjectName("newPassword")
        self.verticalLayout_2.addWidget(self.newPassword, 0, QtCore.Qt.AlignHCenter)
        self.confPassword = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.confPassword.sizePolicy().hasHeightForWidth())
        self.confPassword.setSizePolicy(sizePolicy)
        self.confPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confPassword.setAlignment(QtCore.Qt.AlignCenter)
        self.confPassword.setObjectName("confPassword")
        self.verticalLayout_2.addWidget(self.confPassword, 0, QtCore.Qt.AlignHCenter)
        self.eMail = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.eMail.sizePolicy().hasHeightForWidth())
        self.eMail.setSizePolicy(sizePolicy)
        self.eMail.setAlignment(QtCore.Qt.AlignCenter)
        self.eMail.setObjectName("eMail")
        self.verticalLayout_2.addWidget(self.eMail, 0, QtCore.Qt.AlignHCenter)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Create User"))
        self.newUser.setPlaceholderText(_translate("Dialog", "New Username"))
        self.newPassword.setPlaceholderText(_translate("Dialog", "New Password"))
        self.confPassword.setPlaceholderText(_translate("Dialog", "Confirm Password"))
        self.eMail.setPlaceholderText(_translate("Dialog", "E-Mail"))

