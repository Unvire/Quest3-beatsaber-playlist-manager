from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QWidget, QTableWidget, QTableWidgetItem, QLabel, QFileDialog, QDialog, QMessageBox
from PyQt5.QtWidgets import QInputDialog, QMessageBox
from PyQt5.QtCore import Qt, QMimeData, QByteArray, QItemSelectionModel, QSize
from PyQt5.QtGui import QDrag, QPixmap, QColor
from PyQt5 import uic

import os, sys, threading, platform, subprocess

from beatSaverAPICaller import BeatSaverAPICaller
from beatSaberPlaylist import BeatSaberPlaylist
from beatSaberMap import BeatSaberMap
from byteStringMusicPlayer import ByteStringMusicPlayer
from adbWrapperFactory import AdbWrapperFactory
from tableWidgetWrapper import TableWidgetWrapper

from playlistDataDialog import PlaylistDataDialog
from deletePlaylistsDialog import DeletePlaylistsDialog
from downloadMissingMapsDialog import DownloadMissingMapsDialog
from connectQuestDialog import ConnectQuestDialog

class MainWindow(QMainWindow):
    def __init__(self):
        self.allMapsPlaylist = BeatSaberPlaylist()
        self.playlistInstance = BeatSaberPlaylist()
        self.musicPlayer = ByteStringMusicPlayer()

        self.adbWrapper = AdbWrapperFactory(platform.system())

        self.sortingOrder = 'Upload date'
        self.isConnected = False

        super().__init__()
        uiFilePath = os.path.join(os.getcwd(), 'ui', 'main.ui')
        uic.loadUi(uiFilePath, self)
        
        self.allMapsTable = TableWidgetWrapper(self.allMapsTable)
        self.allMapsTable._setSourceMode(self.sourceTableStartDrag, self.sourceTableRowClicked)

        self.playlistsMapsTable = TableWidgetWrapper(self.playlistsMapsTable)
        self.playlistsMapsTable._setTargetMode(self.targetTableDragEnterEvent, self.targetTableDragMoveEvent, self.targetTableDropEvent, self.targetTableRowClicked)

        header = self.mapLevelsTable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
    
        self.actionNewEmptyPlaylist.triggered.connect(self.blankNewPlaylist)
        self.actionNewFromDownloadedMaps.triggered.connect(self.newPlaylistFromDownloadedSongs)
        self.savePlaylistAction.triggered.connect(self.savePlaylistAs)
        self.loadPlaylistAction.triggered.connect(self.loadPlaylist)

        self.connectAction.triggered.connect(self.connectToQuest)
        self.getSongsFromQuestAction.triggered.connect(self.getSongsFromQuest)
        self.checkMissingMapsAction.triggered.connect(self.checkMissingMaps)
        self.pullPlaylistsFromQuestAction.triggered.connect(self.pullPlaylists)
        self.pushPlaylistsToQuestAction.triggered.connect(self.pushPlaylists)
        self.deletePlaylistsFromQuestAction.triggered.connect(self.deletePlaylists)

        self.action_debug.triggered.connect(self.debugGetSongsFromQuest)

        self.sortAllMapsByComboBox.currentIndexChanged.connect(self.sortAllMapsBy)
        self.reverseSortingOrderButton.clicked.connect(self.reverseAllMapsSorting)

        self.playMusicButton.clicked.connect(self.playMusic)
        self.stopMusicButton.clicked.connect(self.stopMusic)

        self.setPlaylistHeaderButton.clicked.connect(self.openDialogWindow)
        self.selectionUpButton.clicked.connect(self.moveSelectedSongsUp)
        self.selectionDownButton.clicked.connect(self.moveSelectedSongsDown)
        self.selectionDeleteButton.clicked.connect(lambda: self.deleteSelectedSongs(self.playlistsMapsTable))
    
    def checkLibrariesInstalled(self):
        def checkIfFfmpegInstalled() -> bool:
            result = subprocess.run('ffmpeg -version', capture_output=True, text=True).stdout
            firstLine = result.splitlines()[0].lower()
            return 'ffmpeg version' in firstLine

        messageBuilder = []
        isAdbInstalled = self.adbWrapper.checkIfInstalled()
        isFfmpegInstalled = checkIfFfmpegInstalled()
        if not (isAdbInstalled and isFfmpegInstalled):
            adbPath = os.path.join(os.getcwd(), 'adb')
            messageAdb = f'Please download Android Debug Bridge [ADB]:\n  https://developer.android.com/tools/adb\nand unzip it into:\n  {adbPath}'            
            messageFfmpeg = 'Please install FFMPEG:\n  https://www.ffmpeg.org/'

            messageBuilder = [message for isInstalled, message in zip((isAdbInstalled, isFfmpegInstalled), (messageAdb, messageFfmpeg)) if not isInstalled]
            self._infoWarning('\n\n'.join(messageBuilder))
    
    def blankNewPlaylist(self):
        if self._askSaveBeforeClearingPlaylist(self.playlistInstance):
            self.savePlaylistAs()

        self.playlistInstance = BeatSaberPlaylist()
        self.musicPlayer = ByteStringMusicPlayer()

        self._clearTable(self.playlistsMapsTable)
        self._clearTable(self.mapLevelsTable)

        pixmap = QPixmap(QSize(256, 256))
        pixmap.fill(QColor(0, 0, 0, 0))
        self._setMapDetails()
        self._setMapImageAndMusic(pixmap, '', '')
    
    def newPlaylistFromDownloadedSongs(self):
        if self._askSaveBeforeClearingPlaylist(self.playlistInstance):
            self.savePlaylistAs()
            return
        
        folderPath = str(QFileDialog.getExistingDirectory(self, 'Select directory with downloaded songs'))
        if not folderPath:
            return
        
        filesList = os.listdir(folderPath)
        mapIDs = [fileName.split(' ')[0] for fileName in filesList]
        responseDict = self._getResponseJSONFromMapsIDList(mapIDs)
        if not responseDict:
            self._infoWarning('Error with obtaining data from beatsaver.com')
            return

        self.playlistInstance.generateFromResponseDict(responseDict)
        self._updateSongsTable(self.playlistsMapsTable, self.playlistInstance)
    
    def savePlaylistAs(self):
        def continueWithMissingHeader(playlistInstance:BeatSaberPlaylist) -> bool:
            isTitleMissing = not bool(playlistInstance.getPlaylistTitle())
            isAuthorMissing = not bool(playlistInstance.getPlaylistAuthor())
            isImageMissing = not bool(playlistInstance.getImageString())

            strings = ['title', 'author', 'image']
            absenceList = [isTitleMissing, isAuthorMissing, isImageMissing]

            if any(absenceList):
                message = f'Header is missing some data: '
                missingAttributes = [string for isAbsent, string in zip(absenceList, strings) if isAbsent]
                if len(missingAttributes) == 1:
                    message += f'{missingAttributes[0]}. '
                elif len(missingAttributes) == 2:
                    message += f'{missingAttributes[0]} and {missingAttributes[1]}. '
                else:
                    message += f'{missingAttributes[0]}, {missingAttributes[1]} and {missingAttributes[2]}. '
                return self._yesNoWarning(f'{message}Continue?')
            else:
                return True
        
        if self.playlistInstance.isEmpty():
            self._infoWarning('Playlist is empty')
            return
        
        if not continueWithMissingHeader(self.playlistInstance):
            return
        
        fileName, ok = QInputDialog.getText(self, 'Save playlist as:', 'Name of playlist')
        if not (ok and fileName):
            return
        
        fileName = fileName if fileName.endswith('json') else f'{fileName}.json'
        path = os.path.join(os.getcwd(), 'playlists', fileName)
        isOverwriteExistingFile = self._yesNoWarning(f'Playlist {fileName} exists. Overwrite it?') if os.path.exists(path) else True
        if not isOverwriteExistingFile:
            self._infoWarning('File was not saved')
            return 
        
        playlistContent = self.playlistInstance.serializeInstanceToJSON()
        with open(path, 'w') as file:
            file.write(playlistContent)
        self._infoWarning(f'Playlist {fileName} saved')
    
    def loadPlaylist(self):
        if self._askSaveBeforeClearingPlaylist(self.playlistInstance):
            self.savePlaylistAs()

        filePath, _ = QFileDialog.getOpenFileName(self, 'Select playlist', '','BeatSaber playlist(*.json *.bplist)')
        if not filePath:
            return
        
        isSuccess = self.playlistInstance.loadFromFile(filePath)
        if not isSuccess:
            self._infoWarning('Error with obtaining data from beatsaver.com')
            return
        self._updateSongsTable(self.playlistsMapsTable, self.playlistInstance)
    
    def connectToQuest(self):
        connectionDialog = ConnectQuestDialog(self.adbWrapper)
        connectionDialog.show()
        connectionDialog.exec_()
        self.isConnected = connectionDialog.getData()
    
    def getSongsFromQuest(self) -> dict:
        if not self.isConnected:
            self._infoWarning('Quest not connected')
            return
        
        mapIDs = self.adbWrapper.getSongKeysFromQuest()
        self._processAllMapsIds(mapIDs)
    
    def checkMissingMaps(self):
        if not self.isConnected:
            self._infoWarning('Quest not connected')
            return
        
        missingMapsIds = self.allMapsPlaylist.checkMissingSongs(self.playlistInstance)
        if missingMapsIds:
            misingMapsInstances = self.playlistInstance.getSongsByIds(missingMapsIds)
            donwloadDialog = DownloadMissingMapsDialog(misingMapsInstances)
            donwloadDialog.exec_()
        else:
            self._infoWarning('All maps present in Quest')
    
    def debugGetSongsFromQuest(self) -> dict:
        mapIDs = self.__mockGetSongsFromQuest()
        self._processAllMapsIds(mapIDs) 

    def pullPlaylists(self):
        if not self.isConnected:
            self._infoWarning('Quest not connected')
            return
        
        questPlaylists = self.adbWrapper.getPlaylistsNamesFromQuest()
        self.adbWrapper.pullPlaylistsFromQuest(questPlaylists)

    def pushPlaylists(self):
        if not self.isConnected:
            self._infoWarning('Quest not connected')
            return
        
        playlistsLocalFolderPath = os.path.join(os.getcwd(), 'playlists')
        playlists = os.listdir(playlistsLocalFolderPath)
        for playlist in playlists:
            playlistPath = os.path.join(playlistsLocalFolderPath, playlist)
            self.adbWrapper.uploadPlaylistIntoQuest(playlistPath)
        
    def deletePlaylists(self):
        if not self.isConnected:
            self._infoWarning('Quest not connected')
            return
        
        questPlaylists = self.adbWrapper.getPlaylistsNamesFromQuest()
        deleteDialog = DeletePlaylistsDialog(questPlaylists)
        if deleteDialog.exec_() == QDialog.Accepted:
            namesList = deleteDialog.getData()
            self.adbWrapper.deletePlaylistsFromQuest(namesList)
            self._infoWarning('Selected playlists deleted')
    
    def _processAllMapsIds(self, mapIDs:list):
        responseDict = self._getResponseJSONFromMapsIDList(mapIDs)
        if not responseDict:
            self._infoWarning('Error with obtaining data from beatsaver.com')
            return
        
        self.allMapsPlaylist.generateFromResponseDict(responseDict)        
        self.allMapsPlaylist.changeSortingOrder()
        self.allMapsPlaylist.sortPlaylistInPlaceBy('Upload date')
        self._updateSongsTable(self.allMapsTable, self.allMapsPlaylist)

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

    def sourceTableRowClicked(self, row, col):
        selectedRowsList = self.allMapsTable.getSelectedRows()
        if selectedRowsList:
            row = selectedRowsList[0]
            mapInstance = self.allMapsPlaylist[row]
            self.generateMapDetails(mapInstance)
    
    def targetTableRowClicked(self, row, col):
        selectedRowsList = self.playlistsMapsTable.getSelectedRows()
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
        self._updateSongsTable(self.allMapsTable, self.allMapsPlaylist)
    
    def reverseAllMapsSorting(self):
        self.allMapsPlaylist.changeSortingOrder()
        self.allMapsPlaylist.sortPlaylistInPlaceBy(self.sortingOrder)
        
        self._unselectAllRowsInTable(self.allMapsTable)
        self._updateSongsTable(self.allMapsTable, self.allMapsPlaylist)
    
    def playMusic(self):
        self.musicPlayer.play()
    
    def stopMusic(self):
        self.musicPlayer.stop()
    
    def openDialogWindow(self):
        title = self.playlistInstance.getPlaylistTitle()
        author = self.playlistInstance.getPlaylistAuthor()
        image = self.playlistInstance.getImageString()

        dialogWindow = PlaylistDataDialog(title, author, image)
        if dialogWindow.exec_() == QDialog.Accepted:
            response = dialogWindow.getData()
            self.playlistInstance.setPlaylistTitle(response['title'])
            self.playlistInstance.setPlaylistAuthor(response['author'])
            self.playlistInstance.setImageString(response['image'])

    def moveSelectedSongsUp(self):
        self._moveSelectedRowsUpDown(self.playlistsMapsTable, 'up')
    
    def moveSelectedSongsDown(self):
        self._moveSelectedRowsUpDown(self.playlistsMapsTable, 'down')

    def deleteSelectedSongs(self, table:QTableWidget):
        selectedRowsList = table.getSelectedRows(table)
        self.playlistInstance.setSelectedIndexes(selectedRowsList)
        self.playlistInstance.removeSelectedSongs()
        self._updateSongsTable(table, self.playlistInstance)
    
    def resizeEvent(self, event):
        labels = [self.mapTitleLabel, self.mapAuthorLabel, self.mapMapperLabel, self.mapBPMLabel, self.mapLengthLabel, 
                  self.mapRankedStateLabel, self.mapUploadedLabel, self.mapTagsLabel]
        for label in labels:
            text = label.toolTip()
            self._elideLabel(label, text)
        super().resizeEvent(event)
    
    def closeEvent(self, event):
        self.musicPlayer.stop()
        self.adbWrapper.terminateAdb()
        event.accept()

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
    
    def _updateSongsTable(self, table:QTableWidget, playlist:BeatSaberPlaylist):
        self._clearTable(table)
        self._addTableRows(table, playlist)

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

        selectedRowsList = table.getSelectedRows()
        self.playlistInstance.setSelectedIndexes(selectedRowsList)
        functionDict[direction]() #move up or down
        indexes = self.playlistInstance.getSelectedIndexes()

        self._updateSongsTable(table, self.playlistInstance)
        self._selectRowsInTable(table, indexes)

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
        return responseDict

    def _yesNoWarning(self, message:str) -> bool:
        reply = QMessageBox.warning(self, 'Warning', message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return reply == QMessageBox.Yes
    
    def _infoWarning(self, message:str):
        QMessageBox.information(self, 'Info', message, QMessageBox.Ok, QMessageBox.Ok)
    
    def _askSaveBeforeClearingPlaylist(self, playlistInstance:BeatSaberPlaylist) -> bool:
        if not playlistInstance.isEmpty():
            return self._yesNoWarning('Current playlist will be cleared. Do you want to save it?')
        else:
            return False
    
                
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindowInstance = MainWindow()
    mainWindowInstance.show()
    mainWindowInstance.checkLibrariesInstalled()
    sys.exit(app.exec_())