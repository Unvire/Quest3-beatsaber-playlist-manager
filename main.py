from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, QMimeData, QItemSelection, QByteArray, QItemSelectionModel
from PyQt5.QtGui import QDrag, QPixmap, QFont
from PyQt5 import uic

import os, sys

from beatSaverAPICaller import BeatSaverAPICaller
from beatSaberPlaylist import BeatSaberPlaylist
from beatSaberMap import BeatSaberMap
from byteStringMusicPlayer import ByteStringMusicPlayer

class MainWindow(QMainWindow):
    def __init__(self):
        self.allMapsPlaylist = BeatSaberPlaylist()
        self.playlistInstance = BeatSaberPlaylist()
        self.musicPlayer = ByteStringMusicPlayer()
        self.sortingOrder = 'Upload date'

        super().__init__()
        uiFilePath = os.path.join(os.getcwd(), 'ui', 'main.ui')
        uic.loadUi(uiFilePath, self)
        
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

        header = self.mapLevelsTable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        self.actionConnect.triggered.connect(self.getSongsFromQuest)

        self.sortAllMapsByComboBox.currentIndexChanged.connect(self.sortAllMapsBy)
        self.reverseSortingOrderButton.clicked.connect(self.reverseAllMapsSorting)

        self.playMusicButton.clicked.connect(self.playMusic)
        self.stopMusicButton.clicked.connect(self.stopMusic)

        self.selectionUpButton.clicked.connect(self.moveSelectedSongsUp)
        self.selectionDownButton.clicked.connect(self.moveSelectedSongsDown)
        self.selectionDeleteButton.clicked.connect(lambda: self.deleteSelectedSongs(self.playlistsMapsTable))
    
    def getSongsFromQuest(self) -> dict:
        responseJSON = self.__mockGetSongsFromQuest()
        if not responseJSON:
            print('Data from server was not obtained')
            return

        for key, mapJSON in responseJSON.items():
            BeatSaberMapInstance = BeatSaberMap(key)
            BeatSaberMapInstance.getDataFromBeatSaverJSON(mapJSON)
            self.allMapsPlaylist.addSongIfNotPresent(BeatSaberMapInstance)
        
        self.allMapsPlaylist.changeSortingOrder()
        self.allMapsPlaylist.sortPlaylistInPlaceBy('Upload date')
        self._addTableRows(self.allMapsTable, self.allMapsPlaylist)

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

        self.mapAuthorLabel.setText(f'Author: {mapInstance.author}')
        self.mapTitleLabel.setText(f'Title: {mapInstance.title}')
        self.mapMapperLabel.setText(f'Mapper: {mapInstance.mapper}')
        self.mapBPMLabel.setText(f'BPM: {mapInstance.bpm}')
        self.mapLengthLabel.setText(f'Length: {lenthTime}')
        self.mapRankedStateLabel.setText(f'Ranked state: {mapInstance.rankedState}')
        self.mapUploadedLabel.setText(f'Uploaded: {mapInstance.uploaded}')
        self.mapTagsLabel.setText(f'Tags: {", ".join(mapInstance.tagsList)}')
        self._generateMapLevelsTable(mapInstance)

        self.musicPlayer.loadMusicFromUrl(mapInstance.previewUrl)

    def _generateMapLevelsTable(self, mapInstance:BeatSaberMap):
        self._clearTable(self.mapLevelsTable)
        for level in mapInstance.diffs:
            rowCount = self.mapLevelsTable.rowCount()
            self.mapLevelsTable.insertRow(rowCount)
            self.mapLevelsTable.setItem(rowCount, 0, QTableWidgetItem(f'{level.difficulty}'))
            self.mapLevelsTable.setItem(rowCount, 1, QTableWidgetItem(f'{level.characteristic}'))
            self.mapLevelsTable.setItem(rowCount, 2, QTableWidgetItem(f'{level.stars}'))
            self.mapLevelsTable.setItem(rowCount, 3, QTableWidgetItem(f'{level.njs}'))
            self.mapLevelsTable.setItem(rowCount, 4, QTableWidgetItem(f'{level.nps}'))
            self.mapLevelsTable.setItem(rowCount, 5, QTableWidgetItem(f'{level.requiredMods}'))
        self._adjustTableHeight(self.mapLevelsTable)

    def _adjustTableHeight(self, table:QTableWidget):
        MARGIN_HEIGHT = 2
        totalTableHeight = table.horizontalHeader().height()
        for row in range(table.rowCount()):
            totalTableHeight += table.rowHeight(row)
        table.setFixedHeight(totalTableHeight + MARGIN_HEIGHT)

    def _addTableRows(self, table:QWidget, playlist:BeatSaberPlaylist):
        for mapInstance in playlist:
            self._addTableRow(table, mapInstance)

    def _addTableRow(self, table:QWidget, mapInstance:BeatSaberMap):
        lastRowID = table.rowCount()
        table.insertRow(lastRowID)
        newRow = QTableWidgetItem(f'{mapInstance.title} by {mapInstance.author}')
        table.setItem(lastRowID, 0, newRow)

    def sourceTableStartDrag(self, supportedActions):
        drag = QDrag(self)
        mimeData = QMimeData()
        selectedRow = self.allMapsTable.currentRow()
        
        mimeData.setText(f'{selectedRow}')
        drag.setMimeData(mimeData)
        drag.exec_(Qt.CopyAction)    

    def targetTableDropEvent(self, event):
        mapIndex = int(event.mimeData().text())
        mapInstance = self.allMapsPlaylist[mapIndex]
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
        if selectedRowsList:
            row = selectedRowsList[0]
            mapInstance = self.allMapsPlaylist[row]
            self.setMapDetails(mapInstance)
    
    def targetTableOnSelectionChanged(self, selected: QItemSelection, deselected: QItemSelection):
        selectedRowsList = self._getSelectedRowsInTable(self.playlistsMapsTable)
        if len(selectedRowsList) == 1:
            index = selectedRowsList[0]
            mapInstance = self.playlistInstance[index]
            self.setMapDetails(mapInstance)

        self.playlistInstance.setSelectedIndexes(selectedRowsList)
    
    def sortAllMapsBy(self, index:int):        
        self.sortingOrder = self.sortAllMapsByComboBox.itemText(index)
        self.allMapsPlaylist.resetSortingReverseMode()
        self.allMapsPlaylist.sortPlaylistInPlaceBy(self.sortingOrder)
        
        self._unselectAllRowsInTable(self.allMapsTable)
        self._clearTable(self.allMapsTable)
        self._addTableRows(self.allMapsTable, self.allMapsPlaylist)
    
    def reverseAllMapsSorting(self):
        self.allMapsPlaylist.changeSortingOrder()
        self.allMapsPlaylist.sortPlaylistInPlaceBy(self.sortingOrder)
        
        self._unselectAllRowsInTable(self.allMapsTable)    
        self._clearTable(self.allMapsTable)
        self._addTableRows(self.allMapsTable, self.allMapsPlaylist)
    
    def playMusic(self):
        self.musicPlayer.play()
    
    def stopMusic(self):
        self.musicPlayer.stop()
    
    def _getImagePixmap(self, mapInstance:BeatSaberMap) -> QPixmap:
        url = mapInstance.coverUrl
        byteString = BeatSaverAPICaller.getImageByteString(url)
        byteArray = QByteArray(byteString)

        pixmap = QPixmap()
        pixmap.loadFromData(byteArray)
        return pixmap

    def _formatSeconds(self, lengthSeconds:int) -> str:
        minutes, seconds = divmod(lengthSeconds, 60)
        seconds = f'0{seconds}' if seconds < 10 else seconds
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