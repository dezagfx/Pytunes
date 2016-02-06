# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow.resize(1024, 620)
       # MainWindow.setStyleSheet("#MainWindow {background-color: qlineargradient(spread:pad, x1:0.964, y1:0.994318, x2:1, y2:0, stop:1 rgb(0, 191, 143), stop:0 rgb(0, 21, 16));}\n"
#"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 27))
        self.menubar.setObjectName("menubar")
        self.menuHome = QtWidgets.QMenu(self.menubar)
        self.menuHome.setObjectName("menuHome")
        self.menuPlaylists = QtWidgets.QMenu(self.menubar)
        self.menuPlaylists.setObjectName("menuPlaylists")
        self.menuBrowse = QtWidgets.QMenu(self.menubar)
        self.menuBrowse.setObjectName("menuBrowse")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionPlaylist1 = QtWidgets.QAction(MainWindow)
        self.actionPlaylist1.setObjectName("actionPlaylist1")
        self.menuPlaylists.addSeparator()
        self.menubar.addAction(self.menuHome.menuAction())
        self.menubar.addAction(self.menuPlaylists.menuAction())
        self.menubar.addAction(self.menuBrowse.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuHome.setTitle(_translate("MainWindow", "Home"))
        self.menuPlaylists.setTitle(_translate("MainWindow", "Music"))
        self.menuBrowse.setTitle(_translate("MainWindow", "Browse"))
        self.actionPlaylist1.setText(_translate("MainWindow", "Playlist1"))

