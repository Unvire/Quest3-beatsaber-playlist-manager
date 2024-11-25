from PyQt5.QtGui import QDragMoveEvent, QDropEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, QMimeData, QDataStream, QByteArray
from PyQt5.QtGui import QDrag, QPixmap
from PyQt5 import uic

import os, sys
from beatSaverAPICaller import BeatSaverAPICaller
from beatSaberPlaylist import BeatSaberPlaylist
from beatSaberMap import BeatSaberMap

class MainWindow(QMainWindow):
    def __init__(self):
        self.allMapsList = []
        self.playListMaps = []

        super().__init__()
        uiFilePath = os.path.join(os.getcwd(), 'ui', 'main.ui')
        uic.loadUi(uiFilePath, self)

        for table in (self.playlistsMapsTable, self.allMapsTable):
            header = table.horizontalHeader()  
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(1, QHeaderView.Stretch)

        self.allMapsTable.setDragEnabled(True)
        self.allMapsTable.setDragDropMode(QTableWidget.DragOnly)
        self.allMapsTable.startDrag = self.startDrag

        self.playlistsMapsTable.setAcceptDrops(True)
        self.playlistsMapsTable.setDragDropMode(QTableWidget.DropOnly)
        self.playlistsMapsTable.dragEnterEvent = self.dragEnterEvent
        self.playlistsMapsTable.dragMoveEvent = self.dragMoveEvent 
        self.playlistsMapsTable.dropEvent = self.dropEvent
        
        self.actionConnect.triggered.connect(self.getSongsFromQuest)
    
    def getSongsFromQuest(self) -> dict:
        responseJSON = self.__mockGetSongsFromQuest()
        for key, mapJSON in responseJSON.items():
            BeatSaberMapInstance = BeatSaberMap(key)
            BeatSaberMapInstance.getDataFromBeatSaverJSON(mapJSON)
            self.allMapsList.append(BeatSaberMapInstance)
        
        self.updateTable(self.allMapsTable, self.allMapsList)

    def __mockGetSongsFromQuest(self) -> dict:
        mapsIDsPath = os.path.join(os.getcwd(), 'other', 'ls_questSongs.txt')
        with open(mapsIDsPath, 'r', encoding='utf-8') as file:
            buffer = file.readlines()
        songsIDsList = [line.split('\\')[0] for line in buffer]
        return BeatSaverAPICaller.multipleMapsCall(songsIDsList)
    
    def updateTable(self, table:QWidget, mapsList:list[BeatSaberMap]):
        for mapInstance in mapsList:
            self.addTableRow(table, mapInstance)

    def addTableRow(self, table:QWidget, map:BeatSaberMap):
        rowCount = table.rowCount()
        table.insertRow(rowCount)
        table.setItem(rowCount, 0, QTableWidgetItem(f'{map.name}'))
        table.setItem(rowCount, 1, QTableWidgetItem(f'a'))

    def startDrag(self, supportedActions):
        drag = QDrag(self)
        mimeData = QMimeData()
        selectedRow = self.allMapsTable.currentRow()
        
        mimeData.setText(f'{selectedRow}')
        drag.setMimeData(mimeData)
        drag.exec_(Qt.CopyAction)    

    def dropEvent(self, event):
        mapIndex = int(event.mimeData().text())
        mapInstance = self.allMapsList[mapIndex]
        if mapInstance not in self.playListMaps:
            self.playListMaps.append(mapInstance)
            self.addTableRow(self.playlistsMapsTable, mapInstance)
            event.accept()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event):
        event.accept()
    
    def dragEnterEvent(self, event):
        event.accept()

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindowInstance = MainWindow()
    mainWindowInstance.show()

    
    sys.exit(app.exec_())
