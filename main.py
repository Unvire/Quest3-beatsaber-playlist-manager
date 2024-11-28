from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QWidget, QTableWidget, QTableWidgetItem, QLabel, QFileDialog
from PyQt5.QtWidgets import QInputDialog, QMessageBox
from PyQt5.QtCore import Qt, QMimeData, QItemSelection, QByteArray, QItemSelectionModel, QSize
from PyQt5.QtGui import QDrag, QPixmap, QColor
from PyQt5 import uic

import os, sys, threading

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
        self.actionNewEmptyPlaylist.triggered.connect(self.blankNewPlaylist)
        self.actionNewFromDownloadedMaps.triggered.connect(self.newPlaylistFromDownloadedSongs)
        self.savePlaylistAction.triggered.connect(self.savePlaylistAs)

        self.sortAllMapsByComboBox.currentIndexChanged.connect(self.sortAllMapsBy)
        self.reverseSortingOrderButton.clicked.connect(self.reverseAllMapsSorting)

        self.playMusicButton.clicked.connect(self.playMusic)
        self.stopMusicButton.clicked.connect(self.stopMusic)

        self.selectionUpButton.clicked.connect(self.moveSelectedSongsUp)
        self.selectionDownButton.clicked.connect(self.moveSelectedSongsDown)
        self.selectionDeleteButton.clicked.connect(lambda: self.deleteSelectedSongs(self.playlistsMapsTable))
    
    def blankNewPlaylist(self):
        self.allMapsPlaylist = BeatSaberPlaylist()
        self.playlistInstance = BeatSaberPlaylist()
        self.musicPlayer = ByteStringMusicPlayer()

        self._clearTable(self.allMapsTable)
        self._clearTable(self.playlistsMapsTable)
        self._clearTable(self.mapLevelsTable)

        pixmap = QPixmap(QSize(256, 256))
        pixmap.fill(QColor(0, 0, 0, 0))
        self._setMapDetails()
        self._setMapImageAndMusic(pixmap, '', '')
    
    def newPlaylistFromDownloadedSongs(self):
        folderPath = str(QFileDialog.getExistingDirectory(self, 'Select Directory'))
        if not folderPath:
            return
        
        filesList = os.listdir(folderPath)
        mapIDs = [fileName.split(' ')[0] for fileName in filesList]
        responseDict = self._getResponseJSONFromMapsIDList(mapIDs)

        self.playlistInstance.generateFromResponseDict(responseDict)

        self._clearTable(self.playlistsMapsTable)
        self._addTableRows(self.playlistsMapsTable, self.playlistInstance)
    
    def savePlaylistAs(self):
        fileName, ok = QInputDialog.getText(self, "Save playlist as:", "Name of playlist")
        if not(ok and fileName):
            return
        
        fileName = fileName if fileName.endswith('json') else f'{fileName}.json'
        path = os.path.join(os.getcwd(), 'playlists', fileName)
        playlistContent = self.playlistInstance.serializeInstanceToJSON()
        with open(path, 'w') as file:
            file.write(playlistContent)
        QMessageBox.information(self, "Information", f"Playlist saved")
    
    def getSongsFromQuest(self) -> dict:
        mapIDs = self.__mockGetSongsFromQuest()
        responseDict = self._getResponseJSONFromMapsIDList(mapIDs)
        
        self.allMapsPlaylist.generateFromResponseDict(responseDict)        
        self.allMapsPlaylist.changeSortingOrder()
        self.allMapsPlaylist.sortPlaylistInPlaceBy('Upload date')
        self._clearTable(self.allMapsTable)
        self._addTableRows(self.allMapsTable, self.allMapsPlaylist)

    def __mockGetSongsFromQuest(self) -> list[str]:
        mapsIDsPath = os.path.join(os.getcwd(), 'other', 'ls_questSongs.txt')
        with open(mapsIDsPath, 'r', encoding='utf-8') as file:
            buffer = file.readlines()
        songsIDsList = [line.split('\\')[0] for line in buffer]
        return songsIDsList
    
    def generateMapDetails(self, mapInstance:BeatSaberMap):
        thread = threading.Thread(target=self._downloadAndSetImageAndMusic, args=(mapInstance,))
        thread.start()     

        lengthTime = self._formatSeconds(mapInstance.lengthSeconds)
        tags = ", ".join(mapInstance.tagsList)
        self._setMapDetails(author=mapInstance.author, title=mapInstance.title, mapper=mapInstance.mapper, bpm=mapInstance.bpm, lengthTime=lengthTime,
                            rankedState=mapInstance.rankedState, uploaded=mapInstance.uploaded, tags=tags)
        self._generateMapLevelsTable(mapInstance)

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
            self.generateMapDetails(mapInstance)
    
    def targetTableOnSelectionChanged(self, selected: QItemSelection, deselected: QItemSelection):
        selectedRowsList = self._getSelectedRowsInTable(self.playlistsMapsTable)
        if len(selectedRowsList) == 1:
            index = selectedRowsList[0]
            mapInstance = self.playlistInstance[index]
            self.generateMapDetails(mapInstance)

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
    
    def resizeEvent(self, event):
        labels = [self.mapTitleLabel, self.mapAuthorLabel, self.mapMapperLabel, self.mapBPMLabel, self.mapLengthLabel, 
                  self.mapRankedStateLabel, self.mapUploadedLabel, self.mapTagsLabel]
        for label in labels:
            text = label.toolTip()
            self._elideLabel(label, text)
        super().resizeEvent(event)
    
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

    def _setMapDetails(self, author:str='', title:str='', mapper:str='', bpm:str='', lengthTime:str='', rankedState:str='', uploaded:str='', tags:str=''):   
        self._elideLabel(self.mapAuthorLabel, f'Author: {author}')
        self._elideLabel(self.mapTitleLabel, f'Title: {title}')
        self._elideLabel(self.mapMapperLabel, f'Mapper: {mapper}')
        self._elideLabel(self.mapBPMLabel, f'BPM: {bpm}')
        self._elideLabel(self.mapLengthLabel, f'Length: {lengthTime}')
        self._elideLabel(self.mapRankedStateLabel, f'Ranked state: {rankedState}')
        self._elideLabel(self.mapUploadedLabel, f'Uploaded: {uploaded}')
        self._elideLabel(self.mapTagsLabel, f'Tags: {tags}')
    
    def _downloadAndSetImageAndMusic(self, mapInstance:BeatSaberMap):
        pixmap, musicByteStr, fileFormat = self._downloadImageAndMusic(mapInstance)
        self._setMapImageAndMusic(pixmap, musicByteStr, fileFormat)
    
    def _downloadImageAndMusic(self, mapInstance:BeatSaberMap) -> tuple[QPixmap, str, str]:
        pixmap = self._getImagePixmap(mapInstance.coverUrl)
        musicByteStr = self.musicPlayer.downloadMusicFromUrl(mapInstance.previewUrl)
        fileFormat = mapInstance.previewUrl.split('.')[-1]
        return pixmap, musicByteStr, fileFormat
    
    def _setMapImageAndMusic(self, pixmap:QPixmap, musicByteStr:str, fileFormat:str):
        self.mapImageLabel.setPixmap(pixmap)
        self.musicPlayer.loadMusicFromByteStr(musicByteStr, fileFormat)

    def _adjustTableHeight(self, table:QTableWidget):
        MARGIN_HEIGHT = 2        
        maxHeight = self._calculateAvailableSpaceForMapDetailsTable()

        totalTableHeight = table.horizontalHeader().height()
        for row in range(table.rowCount()):
            rowHeight = table.rowHeight(row)
            if totalTableHeight + rowHeight > maxHeight + MARGIN_HEIGHT:
                break
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

    def _formatSeconds(self, lengthSeconds:int) -> str:
        minutes, seconds = divmod(lengthSeconds, 60)
        seconds = f'0{seconds}' if seconds < 10 else seconds
        return f'{minutes}:{seconds}'
    
    def _getImagePixmap(self, imageUrl:str) -> QPixmap:
        byteString = BeatSaverAPICaller.getImageByteString(imageUrl)
        byteArray = QByteArray(byteString)

        pixmap = QPixmap()
        pixmap.loadFromData(byteArray)
        return pixmap
    
    def _elideLabel(self, label:QLabel, text:str):
        label.setToolTip(text)
        labelWidth = label.width()
        fontMetrics = label.fontMetrics()

        if labelWidth > 50:
            elidedText = fontMetrics.elidedText(text, Qt.ElideRight, labelWidth)
        else:
            elidedText = "..."

        label.setText(elidedText)
    
    def _calculateAvailableSpaceForMapDetailsTable(self) -> int:
        tableCoords = self.mapLevelsTable.geometry()
        playButtonCoords = self.playMusicButton.geometry()
        return playButtonCoords.y() - tableCoords.y()
    
    def _getResponseJSONFromMapsIDList(self, listID:list[str]) -> dict:
        responseDict = BeatSaverAPICaller.multipleMapsCall(listID)
        if not responseDict:
            print('Data from server was not obtained')
            return {}
        return responseDict
        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindowInstance = MainWindow()
    mainWindowInstance.show()
    sys.exit(app.exec_())