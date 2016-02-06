import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit
from PyQt5.QtWidgets import QTextEdit, QWidget, QDialog, QApplication, QMainWindow, QTableWidgetItem, QStyle, QMenu, QAction
from PyQt5 import *
import json
import main_ui1
import login_ui
import create_user_ui
import mwindow3_ui
import addplaylist_ui
from config import config
from config import themes
from lib import session_lib, request_lib, server
from gi.repository import Gst, GLib
from random import randint
import time


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
        #response = requests.post(config.server_host+'/auth/create_account', {'name':self.newUser.text(),'password':self.newPassword.text(),'password_confirmation':self.confPassword.text(),'email':self.eMail.text()}, verify=False)
        
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
        #self.setWindowFlags(Qt.FramelessWindowHint);
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
        self.rewindbutton.clicked.connect(self.on_previous)
        self.forwardbutton = self.pushButton_3
        self.forwardbutton.setText("")
        self.forwardbutton.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.forwardbutton.clicked.connect(self.on_next)
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
        self.w = None
     
        
#http://notes.brooks.nu/2011/01/python-gstreamer-controller/
#Usamos esta função para fazer debugging à aplicação e para controlar quando a 
#música chega ao fim dado que sempre que isso acontece é enviada uma mensagem
#GST_MESSAGE_EOS
    def on_slider_seek(self):
        seek_time_secs = self.horizontalSlider_2.value()
        self.playbin.seek_simple(Gst.Format.TIME,  Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, seek_time_secs * Gst.SECOND)
    
    def add_playlist(self):
        self.w = addplaylist(self)
        self.w.show()

    def debugging(self, bus, message):
        debug = message.type
        print(debug)
        if "GST_MESSAGE_EOS" in str(debug):
            self.on_next()
   

    def setVolume(self, value):
        self.horizontalSlider.setValue(value)
        self.playbin.set_property('volume', self.horizontalSlider.value()/100)

        

    def user_playlist(self):
        self.listWidget.clear()
        from PyQt5.QtCore import QVariant
        from PyQt5.QtWidgets import QListWidgetItem
        r = server.getServer('user/playlists', {'token':session_lib.get_token()})
        playlists = r['payload']['playlists']
        self.listWidget.itemDoubleClicked.connect(self.playlist_changed)
        my_item2 = QListWidgetItem()
        my_item2.setText('Browse Music')
        my_item2.setIcon(QIcon("images/browse-music.png"))
        my_item2.setData(Qt.UserRole, 999)
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


    def delete_playlist(self, pid):
        print("DDDDDDDDDDDpid", pid)
        r = server.postServer('playlists/delete', {'playlist_id':int(pid),'token':session_lib.get_token()})
        print(r)

        #if r['success'] is True:
        #time.sleep(2)
        self.user_playlist()

        #else:
          #  print('Erro a apagar a playlist..')

    def get_library(self):
        self.clean_table()
        r = server.getServer('musics/', {'token':session_lib.get_token()})
        if len(r['payload']['musics']) == 0:
            self.clean_table()
        else:
            self.tableWidget.setRowCount(len(r['payload']['musics']))
            self.tableWidget.setColumnCount(1)
            self.tableWidget.setHorizontalHeaderLabels(['Musica'])
            self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.tableWidget.horizontalHeader().setStretchLastSection(True)
            self.tableWidget.cellDoubleClicked.connect(self.select_music)
            i = 0
            self.musics_in_current_playlist_by_index = {}
            for music in r['payload']['musics']:
                self.musics_in_current_playlist_by_index[i] = {
                    'id': music['id'], 'file_name': music['file_name'],
                    'name': music['name']
                }

                musica = QTableWidgetItem(music['name'])
                file_path = QTableWidgetItem(music['file_name'])
                musica.setFlags(musica.flags() & ~Qt.ItemIsEditable)
                self.tableWidget.setItem(i, 0, musica)
                self.tableWidget.setItem(i, 1, file_path)
                i+=1

        
    def playlist_changed(self, arg):
        playlist_id = arg.data(Qt.UserRole)

        if playlist_id == 999:
            self.get_library()

        elif playlist_id is None:
            pass

        else:
            self.show_musics(playlist_id)



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
            i = 0
            self.musics_in_current_playlist_by_index = {}
            for music in r['payload']['musics']:
                self.musics_in_current_playlist_by_index[i] = {
                    'id': music['id'], 'file_name': music['file_name'],
                    'name': music['name']
                }

                musica = QTableWidgetItem(music['name'])
                file_path = QTableWidgetItem(music['file_name'])
                musica.setFlags(musica.flags() & ~Qt.ItemIsEditable)
                self.tableWidget.setItem(i, 0, musica)
                self.tableWidget.setItem(i, 1, file_path)
                i+=1

            

        

    def clean_table(self):
        self.tableWidget.setColumnCount(0)
        self.tableWidget.hideColumn(0)
        self.tableWidget.setRowCount(0)


    def change_state(self):

        if self.is_playing == False:
            self.on_play()

        elif self.is_playing == True:
            self.on_pause()
            
    def select_music(self, i):
        self.playbin.set_state(Gst.State.NULL)
        self.path_musica = self.musics_in_current_playlist_by_index[i]['file_name']
        self.currently_playingID = i
        self.currently_playing = self.musics_in_current_playlist_by_index[self.currently_playingID]['name']
        #self.currently_playingID = i
        self.on_play()
        self.label.setText(self.currently_playing)
       
    def on_play(self):
        #self.playbin.set_property('uri',config.server_host+'/musics/'+self.path_musica)
        if self.path_musica is None:
            pass
        else:
            self.playbin.set_property('uri',config.server_host+'/musics/%s'%self.path_musica)
            self.is_playing = True
            self.playbin.set_state(Gst.State.PLAYING)
            self.playbutton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            #GLib.timeout_add(1000, self.update_slider)
            #self.label.setText("Form","%"% )

    def on_pause(self):
        self.is_playing = False
        self.playbin.set_state(Gst.State.PAUSED)
        self.playbutton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def on_next(self):
        if self.currently_playingID is None:
            pass

        elif self.currently_playingID < len(self.musics_in_current_playlist_by_index)-1:
            self.is_playing = False
            self.playbin.set_state(Gst.State.PAUSED)
            self.currently_playingID += 1
            next_music = self.musics_in_current_playlist_by_index[self.currently_playingID]['file_name']
            self.tableWidget.setCurrentCell(self.currently_playingID, 0)
            self.label.setText(self.musics_in_current_playlist_by_index[self.currently_playingID]['name'])
            self.next(next_music)
            
        else:
            self.currently_playingID = 0
            self.tableWidget.setCurrentCell(self.currently_playingID, 0)
            next_music = self.musics_in_current_playlist_by_index[self.currently_playingID]['file_name']
            self.label.setText(self.musics_in_current_playlist_by_index[self.currently_playingID]['name'])
            self.next(next_music)

    def next(self, next_music):
        self.playbin.set_state(Gst.State.READY)
        self.playbin.set_property('uri',config.server_host+'/musics/'+next_music)
        self.playbin.set_state(Gst.State.PLAYING)

    def on_previous(self, widget):
        if self.currently_playingID is None:
            pass

        elif self.currently_playingID > 0:
            self.is_playing = False
            self.playbin.set_state(Gst.State.PAUSED)
            self.currently_playingID -= 1
            next_music = self.musics_in_current_playlist_by_index[self.currently_playingID]['file_name']
            self.tableWidget.setCurrentCell(self.currently_playingID, 0)
            self.label.setText(self.musics_in_current_playlist_by_index[self.currently_playingID]['name'])
            self.next(next_music)
            
        else:
            self.currently_playingID = 0
            self.tableWidget.setCurrentCell(self.currently_playingID, 0)
            next_music = self.musics_in_current_playlist_by_index[self.currently_playingID]['file_name']
            self.next(next_music)

    def previous(self, next_music):
        self.playbin.set_state(Gst.State.READY)
        self.playbin.set_property('uri',config.server_host+'/musics/'+next_music)
        self.playbin.set_state(Gst.State.PLAYING)
        


        
        #starting up a timer to check on the current playback value
        #GLib.timeout_add(1000, self.update_slider)
        

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

