import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit
from PyQt5.QtWidgets import QTextEdit, QWidget, QDialog, QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import *
import json
import main_ui1
import login_ui
import create_user_ui
from config import config
from config import themes
from lib import session_lib, request_lib, server


######################## CLASSE QUE TRATA DO LOGIN #############################


class Login(QDialog, login_ui.Ui_Dialog):

    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.logincheck)
        self.pushButton_2.clicked.connect(self.criarContaWindow)
        


    def criarContaWindow(self):
        self.hide()
        self.criarConta = criarConta()
        self.criarConta.show()

    def teste(self):
        self.username = str(self.lineEdit.text())
        self.accept()

    def logincheck(self):
        self.username = str(self.lineEdit.text())
        self.password = str(self.lineEdit_2.text())
        if (self.username == "" or self.password == ""):
            QtWidgets.QMessageBox.information(
                self, "Campo Vazio", "Por favor preencha todos os campos."
            )
        
        else:
            
            response, ok = server.postServer(
                    'auth/login', 
                    {'user_name' : self.username,'password' : self.password}
            )
            if response['success'] == True:
                QtWidgets.QMessageBox.information(
                    self, "Sucesso", "Bem vindo/a: %s"% self.username
                )
                session_lib.set_token(response['payload']['token'])
                self.accept()
            else:
                fail= response['error_message']
                messages = "\n".join(fail)
                QtWidgets.QMessageBox.information(self, "Erro", "%s"%messages)

#http://stackoverflow.com/questions/31843262/pass-a-variable-from-one-class-to-another-in-pyqt
#http://bytes.com/topic/python/answers/462303-pyqt-qdialog-qmainwindow-interacting-each-other
    def accept(self):
        self.mainwindow = Pytunes(self.username)
        self.mainwindow.show()
        QDialog.accept(self)


######################## CLASSE PARA CRIAR CONTA ###############################

class criarConta(QDialog, create_user_ui.Ui_Dialog):
#http://stackoverflow.com/questions/30470433/how-to-put-a-child-window-inside-a-main-windowpyqt

    def __init__(self, parent=None):
        super(criarConta, self).__init__(parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.testarConta)
        self.buttonBox.rejected.connect(self.cancelCriarConta)
        #self.raise_()

    def testarConta(self):

        response, ok = server.postServer(
                    'auth/create_account', 
                    {'name':self.newUser.text(),'password':self.newPassword.text(),'password_confirmation':self.confPassword.text(),'email':self.eMail.text()}
            )
        #response = requests.post(config.server_host+'/auth/create_account', {'name':self.newUser.text(),'password':self.newPassword.text(),'password_confirmation':self.confPassword.text(),'email':self.eMail.text()}, verify=False)
        #print (response)
        if response['success'] == True:
            QtWidgets.QMessageBox.information(self, "Sucesso", "Utilizador %s criado"% self.newUser.text())
            self.accept()

        else:
            fail = response['error_message']
            messages = "\n".join(fail)
            QtWidgets.QMessageBox.information(self, "Erro", "%s"%messages)

    def accept(self):
        QDialog.accept(self)
        self.login = Login()
        self.login.show()


    def cancelCriarConta(self):
        self.close()
        self.login = Login()
        self.login.show()



#http://stackoverflow.com/questions/13768012/to-show-pyqt-main-window-inside-a-function


class Pytunes(QMainWindow, main_ui1.Ui_MainWindow):
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


class PlayList(QWidget):
    def __init__(self, parent=None):
        super(PlayList, self).__init__(parent)
        #self.centralwidget = QtWidgets.QWidget(Pytunes)
        #self.tableWidget = QtWidgets.QTableWidget()
        #self.tableWidget.setObjectName("tableWidget")
        self.setupUi(self)
    #def playlistNumber(self):

        entries = [
        {'name':'NomeMusica','artist':'artista'},
        {'name':'NomeMusica','artist':'artista'},
        {'name':'NomeMusica','artist':'artista'},
        {'name':'NomeMusica','artist':'artista'},
        {'name':'NomeMusica','artist':'artista'},
        {'name':'NomeMusica','artist':'artista'},
        {'name':'NomeMusica','artist':'artista'},
        ]



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
    app.setStyleSheet(themes.default_theme)
    app.window().show()
    sys.exit(app.exec_())
