from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QMessageBox
from PyQt5.QtWidgets import QInputDialog, QMessageBox
from PyQt5 import uic

import os, sys, platform, subprocess

from beatSaverAPICaller import BeatSaverAPICaller
from beatSaberPlaylist import BeatSaberPlaylist
from byteStringMusicPlayer import ByteStringMusicPlayer
from adbWrapperFactory import AdbWrapperFactory
from tabletWidgetWrapper import QuestSongsTable, PlaylistSongsTable
from mapDetailsWrapper import MapDetailsWrapper
from labelWrapper import LabelWrapper

from playlistDataDialog import PlaylistDataDialog
from deletePlaylistsDialog import DeletePlaylistsDialog
from downloadMissingMapsDialog import DownloadMissingMapsDialog
from connectQuestDialog import ConnectQuestDialog
from filterMapsDialog import FilterMapsDialog

class MainWindow(QMainWindow):
    def __init__(self):
        self.questMapsPlaylist = BeatSaberPlaylist()
        self.playlistInstance = BeatSaberPlaylist()
        self.musicPlayer = ByteStringMusicPlayer()
        self.adbWrapper = AdbWrapperFactory(platform.system())

        self.sortingOrder = 'Upload date'
        self.isConnected = False

        self.questPreviousSearchParameters = FilterMapsDialog.defaultPreviousSearchParameters()
        self.playlistPreviousParameters = FilterMapsDialog.defaultPreviousSearchParameters()

        super().__init__()
        uiFilePath = os.path.join(os.getcwd(), 'ui', 'main.ui')
        uic.loadUi(uiFilePath, self)

        self.mapAuthorLabel = LabelWrapper(self.mapAuthorLabel)
        self.mapTitleLabel = LabelWrapper(self.mapTitleLabel)
        self.mapMapperLabel = LabelWrapper(self.mapMapperLabel)
        self.mapBPMLabel = LabelWrapper(self.mapBPMLabel)
        self.mapLengthLabel = LabelWrapper(self.mapLengthLabel)
        self.mapRankedStateLabel = LabelWrapper(self.mapRankedStateLabel)
        self.mapUploadedLabel = LabelWrapper(self.mapUploadedLabel)
        self.mapTagsLabel = LabelWrapper(self.mapTagsLabel)
        self.mapLevelsTable = LabelWrapper(self.mapLevelsTable)    

        self.mapDetails = MapDetailsWrapper()
        self.mapDetails.setStaticWidgets(authorLabel=self.mapAuthorLabel, titleLabel=self.mapTitleLabel, mapperLabel=self.mapMapperLabel, 
                                        bpmLabel=self.mapBPMLabel, lengthTimeLabel=self.mapLengthLabel, rankedStateLabel=self.mapRankedStateLabel, 
                                        uploadedLabel=self.mapUploadedLabel, mapTagsLabel=self.mapTagsLabel, levelsTable=self.mapLevelsTable)
        self.mapDetails.setFirstWidgetBelowTable(self.playMusicButton)
        self.mapDetails.setWebRequestWidgets(self.mapImageLabel, self.musicPlayer)
        
        self.questMapsTable = QuestSongsTable(self.questMapsTable, self.questMapsPlaylist, self.mapDetails.update)
        self.playlistMapsTable = PlaylistSongsTable(self.playlistMapsTable, self.playlistInstance, self.mapDetails.update)
        self.playlistMapsTable.setSourcePlaylist(self.questMapsPlaylist)
    
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

        #self.action_debug.triggered.connect(self.debugGetSongsFromQuest)

        self.sortQuestMapsByComboBox.currentIndexChanged.connect(self.sortAllMapsBy)
        self.reverseSortingOrderButton.clicked.connect(self.reverseAllMapsSorting)

        self.playMusicButton.clicked.connect(self.playMusic)
        self.stopMusicButton.clicked.connect(self.stopMusic)

        self.setPlaylistHeaderButton.clicked.connect(self.openPlaylistDataDialogWindow)
        self.selectionUpButton.clicked.connect(self.moveSelectedSongsUp)
        self.selectionDownButton.clicked.connect(self.moveSelectedSongsDown)
        self.selectionDeleteButton.clicked.connect(self.deleteSelectedSongs)

        self.filterQuestMapsButton.clicked.connect(lambda: self.filterMaps(self.questMapsPlaylist, self.questMapsTable, 'quest'))
        self.resetFilterQuestMapsButton.clicked.connect(lambda: self.resetMapsFilter(self.questMapsTable))
        self.filterPlaylistButton.clicked.connect(lambda: self.filterMaps(self.playlistInstance, self.playlistMapsTable, 'playlist'))
        self.resetFilterPlaylistButton.clicked.connect(lambda: self.resetMapsFilter(self.playlistMapsTable))
    
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

        self._clearPlaylist()
    
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
        
        self._clearPlaylist()
        self.playlistInstance.generateFromResponseDict(responseDict)
        self.playlistMapsTable.generateRows()
    
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
        self.playlistMapsTable.generateRows()
    
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
        
        missingMapsIds = self.questMapsPlaylist.checkMissingSongs(self.playlistInstance)
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
        
        self.questMapsPlaylist.generateFromResponseDict(responseDict)        
        self.questMapsPlaylist.changeSortingOrder()
        self.questMapsPlaylist.sortPlaylistInPlaceBy('Upload date')
        self.questMapsTable.generateRows()

    def __mockGetSongsFromQuest(self) -> list[str]:
        mapsIDsPath = os.path.join(os.getcwd(), 'other', 'ls_questSongs.txt')
        with open(mapsIDsPath, 'r', encoding='utf-8') as file:
            buffer = file.readlines()
        songsIDsList = [line.split('\\')[0] for line in buffer]
        return songsIDsList
    
    def sortAllMapsBy(self, index:int):        
        self.sortingOrder = self.sortQuestMapsByComboBox.itemText(index)
        self.questMapsPlaylist.resetSortingReverseMode()
        self.questMapsPlaylist.sortPlaylistInPlaceBy(self.sortingOrder)
        
        self.questMapsTable.unselectAll()
        self.questMapsTable.generateRows()
    
    def reverseAllMapsSorting(self):
        self.questMapsPlaylist.changeSortingOrder()
        self.questMapsPlaylist.sortPlaylistInPlaceBy(self.sortingOrder)
        
        self.questMapsTable.unselectAll()
        self.questMapsTable.generateRows()
    
    def playMusic(self):
        self.musicPlayer.play()
    
    def stopMusic(self):
        self.musicPlayer.stop()
    
    def openPlaylistDataDialogWindow(self):
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
        self.playlistMapsTable.moveSelectedMapsUp()
    
    def moveSelectedSongsDown(self):
        self.playlistMapsTable.moveSelectedMapsDown()

    def deleteSelectedSongs(self):
        self.playlistMapsTable.deleteSelectedMaps()
    
    def filterMaps(self, playlist:BeatSaberPlaylist, table:QuestSongsTable|PlaylistSongsTable, tableName:str):
        settersDict = {
            'quest': self.setQuestPreviousSearchParameters,
            'playlist': self.setPlaylistPreviousSearchParameters
        }

        gettersDict = {
            'quest': self.getQuestPreviousSearchParameters,
            'playlist': self.getPlaylistPreviousSearchParameters
        }

        previousParameters = gettersDict[tableName]()

        dialogWindow = FilterMapsDialog(playlist)
        dialogWindow.setPreviousSearchParameters(previousParameters)
        if dialogWindow.exec_() == QDialog.Accepted:
            indexesToHide = dialogWindow.getHideIndexesList()
            searchParameters = dialogWindow.getPreviousSearchParameters()
            settersDict[tableName](searchParameters)

            if indexesToHide:
                table.hideRows(indexesToHide)
            else:
                self.resetMapsFilter(table)
    
    def setQuestPreviousSearchParameters(self, parametersDict:dict):
        self.questPreviousSearchParameters = parametersDict
    
    def setPlaylistPreviousSearchParameters(self, parametersDict:dict):
        self.playlistPreviousParameters = parametersDict

    def getQuestPreviousSearchParameters(self) -> dict:
        return self.questPreviousSearchParameters
    
    def getPlaylistPreviousSearchParameters(self) -> dict:
        return self.playlistPreviousParameters
    
    def resetMapsFilter(self, table:QuestSongsTable|PlaylistSongsTable):
        table.showAllRows()

    def resizeEvent(self, event):
        self.mapDetails.resize()
        super().resizeEvent(event)
    
    def closeEvent(self, event):
        self.musicPlayer.stop()
        self.adbWrapper.terminateAdb()
        event.accept()
    
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
    
    def _clearPlaylist(self):
        self.playlistInstance = BeatSaberPlaylist()
        self.musicPlayer = ByteStringMusicPlayer()
        self.playlistMapsTable.clear()
        self.mapDetails.resetMapDetails()
    
                
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindowInstance = MainWindow()
    mainWindowInstance.show()
    mainWindowInstance.checkLibrariesInstalled()
    sys.exit(app.exec_())