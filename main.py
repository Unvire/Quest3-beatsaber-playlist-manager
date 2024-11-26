from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, QMimeData, QItemSelection, QByteArray, QItemSelectionModel
from PyQt5.QtGui import QDrag, QPixmap
from PyQt5 import uic

import os, sys

from beatSaverAPICaller import BeatSaverAPICaller
from beatSaberPlaylist import BeatSaberPlaylist
from beatSaberMap import BeatSaberMap

class MainWindow(QMainWindow):
    def __init__(self):
        self.allMapsPlayList = BeatSaberPlaylist()
        self.playlistInstance = BeatSaberPlaylist()

        super().__init__()
        uiFilePath = os.path.join(os.getcwd(), 'ui', 'main.ui')
        uic.loadUi(uiFilePath, self)

        for table in (self.playlistsMapsTable, self.allMapsTable):
            header = table.horizontalHeader()  
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(1, QHeaderView.Stretch)

        self.allMapsTable.setDragEnabled(True)
        self.allMapsTable.setDragDropMode(QTableWidget.DragOnly)
        self.allMapsTable.startDrag = self.sourceTableStartDrag
        self.allMapsTable.selectionModel().selectionChanged.connect(self.sourceTableOnSelectionChanged)

        self.playlistsMapsTable.setAcceptDrops(True)
        self.playlistsMapsTable.setDragDropMode(QTableWidget.DropOnly)
        self.playlistsMapsTable.dragEnterEvent = self.targetTableDragEnterEvent
        self.playlistsMapsTable.dragMoveEvent = self.targetTableDragMoveEvent 
        self.playlistsMapsTable.dropEvent = self.targetTableDropEvent
        self.playlistsMapsTable.selectionModel().selectionChanged.connect(self.targetTableOnSelectionChanged)
        
        self.actionConnect.triggered.connect(self.getSongsFromQuest)

        self.selectionUpButton.clicked.connect(self.moveSelectedSongsUp)
        self.selectionDownButton.clicked.connect(self.moveSelectedSongsDown)
        self.selectionDeleteButton.clicked.connect(lambda: self.deleteSelectedSongs(self.playlistsMapsTable))
    
    def getSongsFromQuest(self) -> dict:
        responseJSON = self.__mockGetSongsFromQuest()
        for key, mapJSON in responseJSON.items():
            BeatSaberMapInstance = BeatSaberMap(key)
            BeatSaberMapInstance.getDataFromBeatSaverJSON(mapJSON)
            self.allMapsPlayList.addSongIfNotPresent(BeatSaberMapInstance)
        
        self._addTableRows(self.allMapsTable, self.allMapsPlayList)

    def __mockGetSongsFromQuest(self) -> dict:
        mapsIDsPath = os.path.join(os.getcwd(), 'other', 'ls_questSongs.txt')
        with open(mapsIDsPath, 'r', encoding='utf-8') as file:
            buffer = file.readlines()
        songsIDsList = [line.split('\\')[0] for line in buffer]
        return BeatSaverAPICaller.multipleMapsCall(songsIDsList)
    
    def setMapDetails(self, mapInstance:BeatSaberMap):
        pixmap = self._getImagePixmap(mapInstance)
        self.mapImageLabel.setPixmap(pixmap)

        lenthTime = self._formatSeconds(mapInstance.lengthSeconds)

        self.songAuthorLabel.setText(f'Author: {mapInstance.author}')
        self.songTitleLabel.setText(f'Title: {mapInstance.title}')
        self.songBPMLabel.setText(f'BPM: {mapInstance.bpm}')
        self.songLengthLabel.setText(f'Length: {lenthTime}')
        self.diffsLabel.setText(f'Levels: {mapInstance.diffs}')
        self.tagsLabel.setText(f'Tags: {mapInstance.tagsList}')

    def _addTableRows(self, table:QWidget, playlist:BeatSaberPlaylist):
        for mapInstance in playlist:
            self._addTableRow(table, mapInstance)

    def _addTableRow(self, table:QWidget, map:BeatSaberMap):
        rowCount = table.rowCount()
        table.insertRow(rowCount)
        table.setItem(rowCount, 0, QTableWidgetItem(f'{map.name}'))
        table.setItem(rowCount, 1, QTableWidgetItem(f'a'))

    def sourceTableStartDrag(self, supportedActions):
        drag = QDrag(self)
        mimeData = QMimeData()
        selectedRow = self.allMapsTable.currentRow()
        
        mimeData.setText(f'{selectedRow}')
        drag.setMimeData(mimeData)
        drag.exec_(Qt.CopyAction)    

    def targetTableDropEvent(self, event):
        mapIndex = int(event.mimeData().text())
        mapInstance = self.allMapsPlayList[mapIndex]
        isMapAdded = self.playlistInstance.addSongIfNotPresent(mapInstance)

        if isMapAdded:
            self._addTableRow(self.playlistsMapsTable, mapInstance)
        event.accept()
    
    def targetTableDragMoveEvent(self, event):
        event.accept()
    
    def targetTableDragEnterEvent(self, event):
        event.accept()

    def sourceTableOnSelectionChanged(self, selected: QItemSelection, deselected: QItemSelection):
        selectedRowsList = self._getSelectedRowsInTable(self.allMapsTable)
        row = selectedRowsList[0]
        mapInstance = self.allMapsPlayList[row]
        self.setMapDetails(mapInstance)
    
    def targetTableOnSelectionChanged(self, selected: QItemSelection, deselected: QItemSelection):
        selectedRowsList = self._getSelectedRowsInTable(self.playlistsMapsTable)
        if len(selectedRowsList) == 1:
            index = selectedRowsList[0]
            mapInstance = self.playlistInstance[index]
            self.setMapDetails(mapInstance)

        self.playlistInstance.setSelectedIndexes(selectedRowsList)
    
    def _getImagePixmap(self, mapInstance:BeatSaberMap) -> QPixmap:
        url = mapInstance.coverUrl
        byteString = BeatSaverAPICaller.getImageByteString(url)
        byteArray = QByteArray(byteString)

        pixmap = QPixmap()
        pixmap.loadFromData(byteArray)
        return pixmap

    def _formatSeconds(self, lengthSeconds:int) -> str:
        minutes, seconds = divmod(lengthSeconds, 60)
        return f'{minutes}:{seconds}'
    
    def moveSelectedSongsUp(self):
        self._moveSelectedRowsUpDown(self.playlistsMapsTable, 'up')
    
    def moveSelectedSongsDown(self):
        self._moveSelectedRowsUpDown(self.playlistsMapsTable, 'down')

    def deleteSelectedSongs(self, table:QTableWidget):
        selectedRowsList = self._getSelectedRowsInTable(table)
        self.playlistInstance.setSelectedIndexes(selectedRowsList)
        self.playlistInstance.removeSelectedSongs()
        self._clearTable(table)
        self._addTableRows(table, self.playlistInstance)
    
    def _moveSelectedRowsUpDown(self, table:QTableWidget, direction:str):
        functionDict = {
            'up': self.playlistInstance.moveSelectedItemsUp,
            'down': self.playlistInstance.moveSelectedItemsDown
        }

        selectedRowsList = self._getSelectedRowsInTable(table)
        self.playlistInstance.setSelectedIndexes(selectedRowsList)
        functionDict[direction]() #move up or down
        indexes = self.playlistInstance.getSelectedIndexes()

        self._clearTable(table)
        self._addTableRows(table, self.playlistInstance)
        self._selectRowsInTable(table, indexes)

    def _getSelectedRowsInTable(self, table:QTableWidget) -> list[int]:
        selectedRows = {index.row() for index in table.selectionModel().selectedIndexes()}
        return list(selectedRows)

    def _unselectAllRowsInTable(self, table:QTableWidget):
        table.selectionModel().clearSelection()
    
    def _selectRowsInTable(self,  table:QTableWidget, indexList:list[int]):
        selectionModelInstance = table.selectionModel()
        for index in indexList:
            selectionModelInstance.select(table.model().index(index, 0), QItemSelectionModel.Rows | QItemSelectionModel.Select)
    
    def _clearTable(self, table:QTableWidget):
        selectionModelInstance = table.model()
        if selectionModelInstance is not None:
            selectionModelInstance.removeRows(0, selectionModelInstance.rowCount())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindowInstance = MainWindow()
    mainWindowInstance.show()
    sys.exit(app.exec_())
