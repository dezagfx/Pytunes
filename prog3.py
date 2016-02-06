import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit
from PyQt5.QtWidgets import QTextEdit, QWidget, QDialog, QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import *
import json
import main_ui1
from config import config
from lib import session_lib, request_lib





######################## CLASSE QUE TRATA DO LOGIN #############################


class Login(QDialog):

    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.logincheck)
        self.pushButton_2.clicked.connect(self.criarContaWindow)

    ################################################################################################################################################
    #
    #                                            PYQT5 STYLING E HUD DO LOGIN()
    #
    #################################################################################################################################################
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(240, 212)
        Dialog.setStyleSheet("#Dialog {\n"
"background-color: qlineargradient(spread:pad, x1:0.964, y1:0.994318, x2:1, y2:0, stop:1 rgb(0, 191, 143), stop:0 rgb(0, 21, 16));\n"
"}")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit, 0, QtCore.Qt.AlignHCenter)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout.addWidget(self.lineEdit_2, 0, QtCore.Qt.AlignHCenter)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton, 0, QtCore.Qt.AlignHCenter)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2, 0, QtCore.Qt.AlignHCenter)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "PyTunes"))
        self.lineEdit.setPlaceholderText(_translate("Dialog", "Username"))
        self.lineEdit_2.setPlaceholderText(_translate("Dialog", "Password"))
        self.pushButton.setText(_translate("Dialog", "Login"))
        self.pushButton_2.setText(_translate("Dialog", "New User"))
    ################################################################################################################################################
    #
    #                                            PYQT5 STYLING E HUD DO LOGIN()
    #
    ################################################################################################################################################

    def criarContaWindow(self):
        self.hide()
        self.criarConta = criarConta()
        self.criarConta.show()

    def teste(self):
        response = requests.post('https://192.168.1.65:8080/auth/login', {'user_name':'ruben','password':'123'}, verify=False)
        #print(self.username,self.password)
        if response.json()['success'] == True:
            print('token->', response.json())


            #session_lib.set_token(response.json()['token'])
            print ('session_lib.token->',session_lib.get_token())
            QtWidgets.QMessageBox.information(self, "Sucesso", "Bem vindo/a: \'%s\'"% self.username)
            self.accept()
        else:
            print ('erro')

    def logincheck(self):
        self.username = str(self.lineEdit.text())
        self.password = str(self.lineEdit_2.text())
        if (self.username == "" or self.password == ""):
            QtWidgets.QMessageBox.information(self, "Campo Vazio", "Por favor preencha todos os campos.")
            return
            #TESTAR LOCALMENTE
            """
            elif (self.username == 'ruben' and
                self.password == '123'):
                QtWidgets.QMessageBox.information(self, "Sucesso", "Bem vindo/a: %s"% self.username)
                self.accept()
            """
        else:
            response = requests.post('https://192.168.1.65:8080/auth/login', {'user_name':self.username,'password':self.password}, verify=False)
            print(self.username,self.password)
            print(response.content)
            if response.json()['success'] == True:
               # print('token->', response.json()['token'])
            

                #session_lib.set_token(response.json()['token'])
                print ('session_lib.token->',session_lib.get_token())
                QtWidgets.QMessageBox.information(self, "Sucesso", "Bem vindo/a: \'%s\'"% self.username)
                self.accept()
            else:
                print ('erro')
#http://stackoverflow.com/questions/31843262/pass-a-variable-from-one-class-to-another-in-pyqt
#http://bytes.com/topic/python/answers/462303-pyqt-qdialog-qmainwindow-interacting-each-other
    def accept(self):
        self.mainwindow = Pytunes(self.username)
        self.mainwindow.show()
        QDialog.accept(self)

          
        
        #CÓDIGO CERTO
        """
        else: 
            response = requests.post(config.server_host+'auth/login', {'user_name':self.lineEdit.text(),'password':self.lineEdit_2.text()}, verify=False)
            if response.json()['success'] == True:
                print('token->', response.json()['token'])
            
            #session_lib.set_token(response.json()['token'])
            print ('session_lib.token->',session_lib.get_token())
            QtWidgets.QMessageBox.information(self, "Sucesso", "Bem vindo/a: \'%s\'"% self.lineEdit.text())
            self.accept()
        """  


######################## CLASSE PARA CRIAR CONTA ###############################

class criarConta(QDialog):
#http://stackoverflow.com/questions/30470433/how-to-put-a-child-window-inside-a-main-windowpyqt

    def __init__(self, parent=None):
        super(criarConta, self).__init__(parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.testarConta)
        self.buttonBox.rejected.connect(self.cancelCriarConta)
        #self.raise_()

    def testarConta(self):

        response = requests.post('https://192.168.1.89:8080/auth/create_account', {'name':self.newUser.text(),'password':self.newPassword.text(),'password_confirmation':self.confPassword.text(),'email':self.eMail.text()}, verify=False)
        print (response.content)
        if response.json()['success'] == True:
            QtWidgets.QMessageBox.information(self, "Sucesso", "Utilizador %s criado"% self.newUser.text())
            self.accept()

        else:
            print('Fail')

    def accept(self):
        QDialog.accept(self)
        self.login = Login()
        self.login.show()


    def cancelCriarConta(self):
        self.close()
        self.login = Login()
        self.login.show()

    ################################################################################################################################################
    #
    #                                            PYQT5 STYLING E HUD DO criarConta()
    #
    #################################################################################################################################################
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(258, 331)
        Dialog.setStyleSheet("#Dialog {\n"
"background-color: qlineargradient(spread:pad, x1:0.964, y1:0.994318, x2:1, y2:0, stop:1 rgb(0, 191, 143), stop:0 rgb(0, 21, 16));\n"
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
        #self.buttonBox.accepted.connect(Dialog.accept)
        #self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Create User"))
        self.newUser.setPlaceholderText(_translate("Dialog", "New Username"))
        self.newPassword.setPlaceholderText(_translate("Dialog", "New Password"))
        self.confPassword.setPlaceholderText(_translate("Dialog", "Confirm Password"))
        self.eMail.setPlaceholderText(_translate("Dialog", "E-Mail"))
    ################################################################################################################################################
    #
    #                                            PYQT5 STYLING E HUD DO criarConta()
    #
    #################################################################################################################################################

  






#http://stackoverflow.com/questions/13768012/to-show-pyqt-main-window-inside-a-function


class Pytunes(QMainWindow):
    def __init__(self, username, parent=None):
        super(Pytunes, self).__init__(parent)
        self.setupUi(self)
        #self.style.setupUi(self)
        #self.playlist()
        self.loggeduser = username
        self.setWindowTitle("Pytunes  Bem-Vindo/a %s"%self.loggeduser)
        #http://stackoverflow.com/questions/21334518/i-need-help-making-a-menu-bar-in-pyqt5
        homeLogOut = self.menuHome.addAction('Logout')
        homeExit = self.menuHome.addAction('Exit')
        homeExit.triggered.connect(self.openPlaylist)
        homeLogOut.triggered.connect(self.openPlaylist)
        self.play_list = PlayList()
        
    

    def exit(self):
        self.close()

    def openPlaylist(self):
        print ('teste teste teste')
        #a = self.play_list.height()
        #b = self.play_list.width()
        self.setCentralWidget(self.play_list)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow.resize(1024, 620)
        MainWindow.setStyleSheet("#MainWindow {background-color: qlineargradient(spread:pad, x1:0.964, y1:0.994318, x2:1, y2:0, stop:1 rgb(0, 191, 143), stop:0 rgb(0, 21, 16));}\n"
"")
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
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../Untitled-1.png"))
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
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
        """
        if self.mdiArea.activeSubWindow() is None:
            self.subwindow.setMinimumSize(b, a)
            self.subwindow.setWidget(self.play_list)
            self.mdiArea.addSubWindow(self.subwindow)
            self.subwindow.show()
            self.subwindow.widget().show()
        """   

    def editor(self):
        self.textEditor = self.playlist()
        self.setCentralWidget(self.textEditor)

    """
    def playlist(self):
        print('ola')
        self.show()
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setObjectName("tableWidget")
        #self.verticalLayout.addWidget(self.tableWidget)
        #self.horizontalLayout.addLayout(self.verticalLayout)

        #CÓDIGO CERTO
        #entries = requests.get(config.server_host+'playlist/'+str(1),verify=False).json() 

        #TESTAR LOCALMENTE
        entries = [{'name':'NomeMusica','artist':'artista'}]



        #with open('data') as input:
        #for d in table_data:

        
        self.tableWidget.setRowCount(len(entries))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['Musica','Artista'])
        i = 0
        for d in entries:
            Musica = QTableWidgetItem(d['name'])
            Artista = QTableWidgetItem(d['artist'])
            #http://nullege.com/codes/search/PyQt5.QtWidgets.QTableWidgetItem.setFlags
            #http://stackoverflow.com/questions/7727863/how-to-make-a-cell-in-a-qtablewidget-read-only
            Musica.setFlags(Musica.flags() & ~Qt.ItemIsEditable)
            Artista.setFlags(Artista.flags() & ~Qt.ItemIsEditable)
            self.tableWidget.setItem(i, 0, Musica)
            self.tableWidget.setItem(i, 1, Artista)
            #QTableWidgetItem.setFlags(QTableWidgetItem.flags() & ~Qt.ItemIsEditable)
            i+=1
        


      
        for i, row in enumerate(entries):
            for j, col in enumerate(row):
                item = QTableWidgetItem(col)
                self.tableWidget.setItem(i, j, item)
        """    
        

"""
class playlist(QWidget):
    def __init__(self, parent=None):
        super(playlist, self).__init__(parent)
        #self.centralwidget = QtWidgets.QWidget(Pytunes)
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setObjectName("tableWidget")

    #def playlistNumber(self):

        entries = [{'name':'NomeMusica','artist':'artista'}]



        #with open('data') as input:
        #for d in table_data:

        
        self.tableWidget.setRowCount(len(entries))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['Musica','Artista'])
        i = 0
        for d in entries:
            Musica = QTableWidgetItem(d['name'])
            Artista = QTableWidgetItem(d['artist'])
            #http://nullege.com/codes/search/PyQt5.QtWidgets.QTableWidgetItem.setFlags
            #http://stackoverflow.com/questions/7727863/how-to-make-a-cell-in-a-qtablewidget-read-only
            Musica.setFlags(Musica.flags() & ~Qt.ItemIsEditable)
            Artista.setFlags(Artista.flags() & ~Qt.ItemIsEditable)
            self.tableWidget.setItem(i, 0, Musica)
            self.tableWidget.setItem(i, 1, Artista)
            #QTableWidgetItem.setFlags(QTableWidgetItem.flags() & ~Qt.ItemIsEditable)
            i+=1
"""

class PlayList(QWidget):
    def __init__(self, parent=None):
        super(PlayList, self).__init__(parent)
        #self.centralwidget = QtWidgets.QWidget(Pytunes)
        #self.tableWidget = QtWidgets.QTableWidget()
        #self.tableWidget.setObjectName("tableWidget")
        self.setupUi(self)
    #def playlistNumber(self):

        entries = [{'name':'NomeMusica','artist':'artista'}]



        #with open('data') as input:
        #for d in table_data:

        
        self.tableWidget.setRowCount(len(entries))
        self.tableWidget.setColumnCount(2)
        #http://nullege.com/codes/show/src@p@y@pyqt5-HEAD@examples@dialogs@findfiles.py/193/PyQt5.QtWidgets.QTableWidget.setSelectionBehavior
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setHorizontalHeaderLabels(['Musica','Artista'])
        i = 0
        for d in entries:
            Musica = QTableWidgetItem(d['name'])
            Artista = QTableWidgetItem(d['artist'])
            #http://nullege.com/codes/search/PyQt5.QtWidgets.QTableWidgetItem.setFlags
            #http://stackoverflow.com/questions/7727863/how-to-make-a-cell-in-a-qtablewidget-read-only
            Musica.setFlags(Musica.flags() & ~Qt.ItemIsEditable)
            Artista.setFlags(Artista.flags() & ~Qt.ItemIsEditable)
            self.tableWidget.setItem(i, 0, Musica)
            self.tableWidget.setItem(i, 1, Artista)
            #QTableWidgetItem.setFlags(QTableWidgetItem.flags() & ~Qt.ItemIsEditable)
            i+=1




    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(720, 347)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.horizontalLayout.addWidget(self.tableWidget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


#http://stackoverflow.com/questions/26603540/how-to-avoid-the-child-qmainwindow-disappearing
#UTIL SE O UTILIZADOR JÁ TIVER O COOKIE DE SESSÃO VÁLIDO PASSA LOGO PARA A MAINWINDOW
#TIVE QUE FAZER SUBCLASS DA APPLICATION()
class Application(QApplication):
    def __init__(self):
        QApplication.__init__(self, sys.argv)
        self._window = None

    def window(self):
        if self._window is None:
            self._window = Login()
        return self._window




if __name__ == '__main__':
    
    app = QApplication = Application()
    app.window().show()
    sys.exit(app.exec_())

