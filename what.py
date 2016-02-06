from PyQt5.QtWidgets import QMainWindow,QTableWidgetItem,QCheckBox
from PyQt5 import QtCore 
from ui.mainwindow import Ui_MainWindow
from item import Item
import re
from collections import Counter
import webbrowser

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self,app,appraiser):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.searchUrl = "";
        self.app = app
        self.appraiser = appraiser;
        self.clipboard = app.clipboard()
        self.objThread = 0
        self.initStatsList()

        self.sBSearchCutUpper.setValue(app.settings.value('search_cut_upper', 115))
        self.sBSearchCutLower.setValue(app.settings.value('search_cut_lower', 85))
        self.cbLeagues.addItem('Standard')
        self.cbLeagues.addItem('Hardcore')
        self.cbLeagues.addItem('Nemesis')
        self.cbLeagues.addItem('Domination')
        self.cbLeagues.setCurrentIndex(app.settings.value('search_league', 0))


        self.sBSearchCutUpper.valueChanged.connect(self.updateSettings)
        self.sBSearchCutLower.valueChanged.connect(self.updateSettings)
        self.cbLeagues.currentIndexChanged.connect(self.updateSettings)
        self.cbLeagues.currentIndexChanged.connect(self.onDataChanged)
        self.clipboard.dataChanged.connect(self.onDataChanged)
        self.clbOpenSearchResults.clicked.connect(self.openSearchResults)
    def onDataChanged(self):
        try:
            self.currentItem = Item(self.clipboard.text())
        except:
            self.statusBar().showMessage("No item in clipboard")
        else:
            if self.currentItem.rarity == 'unknown': return
            self.showItemStats(self.currentItem)
            self.lblItemName.setText(self.currentItem.item_name)
            weight = self.appraiser.weight(self.currentItem)
            self.lblItemScore.setText("%0.2f" % weight)
            self.performSearch()
            try:
                self.statusBar().showMessage("")
            except:
                self.statusBar().showMessage("Error fetching prices")
                pass   

    def openSearchResults(self):
        if (self.searchUrl != ""):
            webbrowser.open(self.searchUrl, 2) 
    def formatPrices(self, prices):
        if (len(prices) == 0):
            return 'No results found, try unchecking mods on the left or widening the cuts.'
        return "\n".join(["%s: %s" % (str(item)[2:-1], value) for item,value in Counter(prices).items()])

    def updateSettings(self):
        self.app.settings.setValue('search_cut_upper',self.sBSearchCutUpper.value())
        self.app.settings.setValue('search_cut_lower',self.sBSearchCutLower.value())
        self.app.settings.setValue('search_league',self.cbLeagues.currentIndex())
        self.app.settings.sync()

    def initStatsList(self):
        self.twItemStats.setColumnCount(4)
        self.twItemStats.setHorizontalHeaderLabels(['', 'Stat', 'Value', 'Type'])

    def showItemStats(self, item):
        while self.twItemStats.rowCount() > 0:
            self.twItemStats.removeRow(0)
        for i, mod in enumerate(item.explicit_mods):
            self.twItemStats.insertRow(i)
            cellWidget = QCheckBox()
            cellWidget.setTristate(0)
            cellWidget.setCheckState(2)
            cellWidget.stateChanged.connect(self.performSearch)
            self.twItemStats.setCellWidget(i,0,cellWidget)
            self.twItemStats.setItem(i,1,QTableWidgetItem(mod.POEXYZNAME))
            self.twItemStats.setItem(i,2,QTableWidgetItem("%0.0f" % mod.value))
            self.twItemStats.setItem(i,3,QTableWidgetItem(mod.AFFIX))

            self.twItemStats.resizeColumnsToContents() 
            self.twItemStats.resizeRowsToContents() 
    def performSearch(self):
        self.statusBar().showMessage("Getting Prices")
        ignoredMods = [i for i in range(self.twItemStats.rowCount()) if self.twItemStats.cellWidget(i,0).checkState() == 0]
        league = self.cbLeagues.currentText()
        
        if (self.objThread):
            if(self.objThread.isRunning()):
                self.searchWorker.finished.connect(self.performSearch)
                return

        self.objThread = QtCore.QThread()
        self.searchWorker = SearchWorker(self. appraiser, self.currentItem,self.sBSearchCutLower.value(),self.sBSearchCutUpper.value(), league, ignoredMods)
        self.searchWorker.moveToThread(self.objThread)
        self.searchWorker.finished.connect(self.searchFinished)
        self.searchWorker.finished.connect(self.objThread.quit)
        self.objThread.started.connect(self.searchWorker.search)
        self.objThread.start()

    def searchFinished(self,url, prices):
        self.searchUrl = url
        self.lblPrices.setText(self.formatPrices(prices))
class SearchWorker(QtCore.QObject):

    finished = QtCore.pyqtSignal(object, object)
    def __init__(self,appraiser, item, undercut, uppercut, league, ignoredMods):
        QtCore.QObject.__init__(self)
        self.appraiser = appraiser
        self.item = item
        self.undercut = undercut
        self.uppercut = uppercut
        self.league = league
        self.ignoredMods = ignoredMods
    def search(self):
        url, prices = self.appraiser.get_prices(self.item, self.undercut, self.uppercut, self.league, self.ignoredMods)
        self.finished.emit(url, prices)