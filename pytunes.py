######################################IMPORT###################################
import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit
from PyQt5.QtWidgets import QTextEdit, QWidget, QDialog, QApplication, QMainWindow, QTableWidgetItem, QStyle, QMenu, QAction
from PyQt5 import *
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QListWidgetItem
import json
import main_ui1
import login_ui
import create_user_ui
import mwindow3_ui
import addplaylist_ui
import add_music_to_playlist_ui
from config import config
from config import themes
from lib import session_lib, request_lib, server
from gi.repository import Gst, GLib
from random import randint
import time

################################################################################

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
            messages = "Preencha todos os campos."
            self.label.setStyleSheet("color: red")
            self.label.setText("%s"%messages)
        
        else:
            
            response, ok = server.postServer(
                    'auth/login', 
                    {'user_name' : self.username,'password' : self.password}
            )
            if response['success'] == True:
               # QtWidgets.QMessageBox.information(
               #     self, "Sucesso", "Bem vindo/a: %s"% self.username
               # )
                self.label.setText("Loggin in...")
                session_lib.set_token(response['payload']['token'])
                self.label.setStyleSheet("color: green")
                self.accept()
            else:
                messages = "Login Inválido"
                self.label.setStyleSheet("color: red")
                self.label.setText("%s"%messages)

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

    def testarConta(self):

        response, ok = server.postServer(
                    'auth/create_account', 
                    {'name':self.newUser.text(),'password':self.newPassword.text(),'password_confirmation':self.confPassword.text(),'email':self.eMail.text()}
            )

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
        self.loggeduser = username
        self.setWindowTitle("Pytunes - CET02 Project")
#http://stackoverflow.com/questions/21334518/i-need-help-making-a-menu-bar-in-pyqt5
        homeLogOut = self.menuHome.addAction('Logout')
        homeExit = self.menuHome.addAction('Exit')
        homeExit.triggered.connect(self.exit)
        homeLogOut.triggered.connect(self.logout)
        self.play_list = user_interface(username)
        self.setCentralWidget(self.play_list)

        

    def logout(self):
        session_lib.del_token()
        self.close()
        self.login = Login()
        self.login.show()
        

    def exit(self):
        self.close()

class user_interface(QWidget, mwindow3_ui.Ui_Form):
    def __init__(self, username, parent=None):
        super(user_interface, self).__init__(parent)
        self.setupUi(self)
        self.user_playlist()
        self.playbutton = self.pushButton_2
        self.playbutton.setText("")
        self.is_playing = False
        self.currently_playingID = None
        self.path_musica = None
        self.playbutton.clicked.connect(self.change_state)
        self.playbutton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.rewindbutton = self.pushButton
        self.rewindbutton.setText("")
        self.rewindbutton.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.rewindbutton.clicked.connect(self.previous_music)
        self.forwardbutton = self.pushButton_3
        self.forwardbutton.setText("")
        self.forwardbutton.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.forwardbutton.clicked.connect(self.next_music)
        self.horizontalSlider.setTickInterval(10)
        self.horizontalSlider.setSingleStep(1)
        self.horizontalSlider.valueChanged.connect(self.setVolume)
        self.label_4.setText("Welcome %s"%username)
        self.playbin = Gst.ElementFactory.make("playbin", "playbin")
        self.addplaylist_button = self.pushButton_4
        self.addplaylist_button.clicked.connect(self.add_playlist)
        self.bus = self.playbin.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.debugging)
        self.addplaylist_popup = None

#http://notes.brooks.nu/2011/01/python-gstreamer-controller/
#Usamos esta função para fazer debugging à aplicação e para controlar quando a 
#música chega ao fim dado que sempre que isso acontece é enviada uma mensagem
#GST_MESSAGE_EOS
    
    def user_playlist(self):
        self.listWidget.clear()
        r = server.getServer('user/playlists', {'token':session_lib.get_token()})
        playlists = r['payload']['playlists']
        self.listWidget.itemClicked.connect(self.playlist_changed)
        my_item2 = QListWidgetItem()
        my_item2.setText('Browse Music')
        my_item2.setIcon(QIcon("images/browse-music.png"))
        my_item2.setData(Qt.UserRole, 0)
        self.listWidget.addItem(my_item2)
        #http://stackoverflow.com/questions/13536839/qt-how-to-improve-my-contextmenu
        self.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget.customContextMenuRequested.connect(self.handleContext)
        for p in playlists:
            my_item=QListWidgetItem()
            my_item.setText(p['name'])
            self.listWidget.addItem(my_item)

            myObject=str(p['id'])
            my_item.setIcon(QIcon("images/playlist-icon.png"))   
            my_item.setData(Qt.UserRole, myObject)

    #http://stackoverflow.com/questions/13536839/qt-how-to-improve-my-contextmenu
    def handleContext(self, pos):
        item = self.listWidget.itemAt(pos)
        itemrow = self.listWidget.row(self.listWidget.itemAt(pos))

        if item is not None and itemrow is not 0:
            itemid = item.data(Qt.UserRole)
            itemname = str(item.text())
            menu = QMenu("Context menu", self)
            #http://eli.thegreenplace.net/2011/04/25/passing-extra-arguments-to-pyqt-slot
            #http://www.thehackeruniversity.com/2014/02/20/pyqt5-beginner-tutorial-part-3/
            delete = QAction(QIcon("images/delete-playlist.png"), "Delete: '%s'"%itemname, self)
            menu.addAction(delete)
            print("#############itemid", itemid)
            delete.triggered.connect(lambda: self.delete_playlist(itemid))
            menu.exec_(self.listWidget.mapToGlobal(pos))

    def add_playlist(self):
        self.addplaylist_popup = addplaylist(self)
        self.addplaylist_popup.show()

    def delete_playlist(self, pid):
        r = server.postServer('playlists/delete', {'playlist_id':int(pid),'token':session_lib.get_token()})
        self.user_playlist()

    def playlist_changed(self, arg):
        playlist_id = arg.data(Qt.UserRole)

        if playlist_id == 0:
            self.get_library()

        elif playlist_id is None:
            pass

        else:
            self.show_musics(playlist_id)

    def debugging(self, bus, message):
        debug = message.type
        print(debug)
        if "GST_MESSAGE_EOS" in str(debug):
            self.on_next()
   

    def setVolume(self, value):
        self.horizontalSlider.setValue(value)
        self.playbin.set_property('volume', self.horizontalSlider.value()/100)

    def show_musics(self, playmid):
        self.clean_table()
        r = server.getServer('playlists/'+playmid, {'id':playmid})
#http://nullege.com/codes/show/src@p@y@pyqt5-HEAD@examples@dialogs@findfiles.py/193/PyQt5.QtWidgets.QTableWidget.setSelectionBehavior
       
        if len(r['payload']['musics']) == 0:
            self.clean_table()
        else:
            self.tableWidget.setRowCount(len(r['payload']['musics']))
            self.tableWidget.setColumnCount(1)
            self.tableWidget.setHorizontalHeaderLabels(['Musica'])
            self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.tableWidget.horizontalHeader().setStretchLastSection(True)
            self.tableWidget.cellDoubleClicked.connect(self.select_music)
            row = 0
            self.musics_in_current_playlist_by_index = {}
            for music in r['payload']['musics']:
                self.musics_in_current_playlist_by_index[row] = {
                    'id': music['id'], 'file_name': music['file_name'],
                    'name': music['name']
                }

                musica = QTableWidgetItem(music['name'])
                file_path = QTableWidgetItem(music['file_name'])
                musica.setFlags(musica.flags() & ~Qt.ItemIsEditable)
                self.tableWidget.setItem(row, 0, musica)
                self.tableWidget.setItem(row, 1, file_path)
                row+=1

    def clean_table(self):
        self.tableWidget.setColumnCount(0)
        self.tableWidget.hideColumn(0)
        self.tableWidget.setRowCount(0)

    def get_library(self):
        from functools import partial 
        self.clean_table()
        r = server.getServer('musics/', {'token':session_lib.get_token()})
        if len(r['payload']['musics']) == 0:
            self.clean_table()
        else:
            self.tableWidget.setRowCount(len(r['payload']['musics']))
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setHorizontalHeaderLabels(['Add to Playlist','Musica'])
            #self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.tableWidget.horizontalHeader().setStretchLastSection(True)
            self.tableWidget.cellDoubleClicked.connect(self.select_music)
            row = 0
            self.musics_in_current_playlist_by_index = {}
            for music in r['payload']['musics']:
                self.musics_in_current_playlist_by_index[row] = {
                    'id': music['id'], 'file_name': music['file_name'],
                    'name': music['name']
                }
                #add_to_playlist = QTableWidgetItem()
                #add_to_playlist.setIcon(QIcon("images/playlist-icon.png"))
                musica = QTableWidgetItem(music['name'])
                file_path = QTableWidgetItem(music['file_name'])
                musica.setFlags(musica.flags() & ~Qt.ItemIsEditable)
                self.tableWidget.setItem(row, 1, musica)
                #self.tableWidget.setItem(row, 1, file_path)
                #self.tableWidget.setItem(row, 0, add_to_playlist)
                #add_to_playlist_button = QtWidgets.QPushButton('Add')
                add_to_playlist_button = QtWidgets.QPushButton('Add')
                add_to_playlist_button.setIcon(QIcon("images/add-to-playlist.png"))
                self.tableWidget.setCellWidget(row,0,add_to_playlist_button)
                add_to_playlist_button.clicked.connect(self.handle_music_to_p)
                #cbk = partial(self.lol, add_to_playlist_button)
                #button.clicked.connect(cbk)
                #add_to_playlist_button.clicked.connect(cbk)
                row+=1

    def handle_music_to_p(self):
        clickme = QtWidgets.QApplication.focusWidget()
        index = self.tableWidget.indexAt(clickme.pos())
        if index.isValid():
            music_id = self.musics_in_current_playlist_by_index[index.row()]['id']
            self.add_m_to_p = add_music_to_playlist(music_id)
            self.add_m_to_p.show()

        

    def select_music(self, row):
        self.playbin.set_state(Gst.State.NULL)
        self.currently_playingID = row
        music_name = self.musics_in_current_playlist_by_index[row]['name']
        music_path = self.musics_in_current_playlist_by_index[row]['file_name']
        self.play_music(music_path)
        self.label.setText(music_name)

    def play_music(self, music_path):
        if music_path is None:
            pass
        else:
            print(music_path,"######2")
            self.playbin.set_property('uri',config.server_host+'/musics/%s'%music_path)
            self.is_playing = True
            self.playbin.set_state(Gst.State.PLAYING)
            self.playbutton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

    def pause_music(self):
        self.is_playing = False
        self.playbin.set_state(Gst.State.PAUSED)
        self.playbutton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def next_music(self):
        print("#####3",self.currently_playingID)
        if self.currently_playingID is None:
            pass

        elif self.currently_playingID < len(self.musics_in_current_playlist_by_index)-1:
            self.playbin.set_state(Gst.State.NULL)
            self.currently_playingID += 1
            next_music = self.musics_in_current_playlist_by_index[self.currently_playingID]['file_name']
            self.tableWidget.setCurrentCell(self.currently_playingID, 0)
            self.label.setText(self.musics_in_current_playlist_by_index[self.currently_playingID]['name'])
            print("##########4",self.currently_playingID)
            print(next_music,"#######1")
            self.play_music(next_music)
            
        else:
            self.currently_playingID = 0
            self.tableWidget.setCurrentCell(self.currently_playingID, 0)
            next_music = self.musics_in_current_playlist_by_index[self.currently_playingID]['file_name']
            self.label.setText(self.musics_in_current_playlist_by_index[self.currently_playingID]['name'])
            self.play_music(next_music)

    def previous_music(self):
        if self.currently_playingID is None:
            pass

        elif self.currently_playingID > 0:
            self.playbin.set_state(Gst.State.NULL)
            self.currently_playingID -= 1
            next_music = self.musics_in_current_playlist_by_index[self.currently_playingID]['file_name']
            self.tableWidget.setCurrentCell(self.currently_playingID, 0)
            self.label.setText(self.musics_in_current_playlist_by_index[self.currently_playingID]['name'])
            self.play_music(next_music)
            
        else:
            self.currently_playingID = 0
            self.playbin.set_state(Gst.State.NULL)
            self.tableWidget.setCurrentCell(self.currently_playingID, 0)
            next_music = self.musics_in_current_playlist_by_index[self.currently_playingID]['file_name']
            self.play_music(next_music)


    def change_state(self):

        if self.is_playing == False:
            self.is_playing = True
            self.playbin.set_state(Gst.State.PLAYING)
            self.playbutton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

        elif self.is_playing == True:
            self.is_playing = False
            self.playbin.set_state(Gst.State.PAUSED)
            self.playbutton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

class addplaylist(QWidget, addplaylist_ui.Ui_Form):
    def __init__(self, m, parent=None):
        #QWidget.__init__(self, parent)
        super(addplaylist, self).__init__(parent)
        self.user_interface = m
        self.setupUi(self)
        self.pushButton.clicked.connect(self.addbutton)

    def addbutton(self):
        playlist_name = self.lineEdit.text()
        print(playlist_name)
        response, ok = server.postServer(
                    'playlists/add', 
                    {'playlist_name':playlist_name, 'token':session_lib.get_token()}
            )
        print(response)

        if response['success'] == True:
            self.close()
            time.sleep(0.05)
            self.user_interface.user_playlist()

class add_music_to_playlist(QWidget, add_music_to_playlist_ui.Ui_Form):
    def __init__(self, mid, parent=None):
        super(add_music_to_playlist, self).__init__(parent)
        self.music_id = mid
        self.setupUi(self)
        self.populate()

    def populate(self):
        self.comboBox.clear()
        r = server.getServer('user/playlists', {'token':session_lib.get_token()})
        playlists = r['payload']['playlists']
        for p in playlists:
            self.comboBox.addItem(p['name'],(p['id']))
        self.pushButton.clicked.connect(self.add_to_playlist)
            

    def add_to_playlist(self):
        playlist_id = self.comboBox.itemData(self.comboBox.currentIndex())
        #print(self.comboBox.itemData(self.comboBox.currentIndex()))
        r, ok = server.postServer("playlists/"+str(playlist_id)+"/add_music", {'token':session_lib.get_token(), 'music_id':self.music_id})
        print(r)
        if r['success'] is True:
            self.close()
    


#http://stackoverflow.com/questions/26603540/how-to-avoid-the-child-qmainwindow-disappearing
#UTIL SE O UTILIZADOR JÁ TIVER O COOKIE DE SESSÃO VÁLIDO PASSA LOGO PARA A MAINWINDOW
#TIVE QUE FAZER SUBCLASS DA APPLICATION()
class Application(QApplication):
    def __init__(self):
        QApplication.__init__(self, sys.argv)
        self._window = None

    def window(self):
        if self._window is None:

            if session_lib.get_token() == "":
                self._window = Login()
                return self._window
            else:
                response, ok = server.postServer(
                    'auth/check_token', 
                    {'token' : session_lib.get_token()}
                )
                if response['success'] == True:
                    username = response['payload']['user']['name']
                    self._window = Pytunes(username)

                else:
                    print('fail')

        return self._window

if __name__ == '__main__':
    
    app = QApplication = Application()
    app.setStyleSheet(themes.default_theme)
    Gst.init()
    app.window().show()
    sys.exit(app.exec_())