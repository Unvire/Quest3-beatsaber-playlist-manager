from PyQt5.QtWidgets import QLabel, QTableWidget, QTableWidgetItem, QMainWindow, QHeaderView
from PyQt5.QtCore import Qt

from beatSaberMap import BeatSaberMap

class MapDetailsWrapper:
    def __init__(self, authorLabel:QLabel, titleLabel:QLabel, mapperLabel:QLabel, bpmLabel:QLabel, lengthTimeLabel:QLabel, 
                 rankedStateLabel:QLabel, uploadedLabel:QLabel, mapTagsLabel:QLabel, levelsTable:QTableWidget):
        self.mapAuthorLabel = authorLabel
        self.mapTitleLabel = titleLabel
        self.mapMapperLabel = mapperLabel
        self.mapBPMLabel = bpmLabel
        self.mapLengthLabel = lengthTimeLabel
        self.mapRankedStateLabel = rankedStateLabel
        self.mapUploadedLabel = uploadedLabel
        self.mapTagsLabel = mapTagsLabel

        self.mapLevelsTable = levelsTable
        header = self.mapLevelsTable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
    
    def update(self, mapInstance:BeatSaberMap, mainWindow:QMainWindow):
        lengthTime = self._formatSeconds(mapInstance.lengthSeconds)
        tags = ", ".join(mapInstance.tagsList)
        self._updateLabels(author=mapInstance.author, title=mapInstance.title, mapper=mapInstance.mapper, bpm=mapInstance.bpm, lengthTime=lengthTime,
                            rankedState=mapInstance.rankedState, uploaded=mapInstance.uploaded, tags=tags)
        self._updateTable(mapInstance, mainWindow)
    
    def _formatSeconds(self, lengthSeconds:int) -> str:
        minutes, seconds = divmod(lengthSeconds, 60)
        seconds = f'0{seconds}' if seconds < 10 else seconds
        return f'{minutes}:{seconds}'

    def _updateLabels(self, author:str='', title:str='', mapper:str='', bpm:str='', lengthTime:str='', rankedState:str='', uploaded:str='', tags:str=''):
        self._elideLabel(self.mapAuthorLabel, f'Author: {author}')
        self._elideLabel(self.mapTitleLabel, f'Title: {title}')
        self._elideLabel(self.mapMapperLabel, f'Mapper: {mapper}')
        self._elideLabel(self.mapBPMLabel, f'BPM: {bpm}')
        self._elideLabel(self.mapLengthLabel, f'Length: {lengthTime}')
        self._elideLabel(self.mapRankedStateLabel, f'Ranked state: {rankedState}')
        self._elideLabel(self.mapUploadedLabel, f'Uploaded: {uploaded}')
        self._elideLabel(self.mapTagsLabel, f'Tags: {tags}')
    
    def _updateTable(self, mapInstance:BeatSaberMap, mainWindow:QMainWindow):
        self._clearTable()
        for level in mapInstance.diffs:
            rowCount = self.mapLevelsTable.rowCount()
            self.mapLevelsTable.insertRow(rowCount)
            self.mapLevelsTable.setItem(rowCount, 0, QTableWidgetItem(f'{level.difficulty}'))
            self.mapLevelsTable.setItem(rowCount, 1, QTableWidgetItem(f'{level.characteristic}'))
            self.mapLevelsTable.setItem(rowCount, 2, QTableWidgetItem(f'{level.stars}'))
            self.mapLevelsTable.setItem(rowCount, 3, QTableWidgetItem(f'{level.njs}'))
            self.mapLevelsTable.setItem(rowCount, 4, QTableWidgetItem(f'{level.nps}'))
            self.mapLevelsTable.setItem(rowCount, 5, QTableWidgetItem(f'{level.requiredMods}'))
        self._adjustTableHeight(mainWindow)
    
    def _clearTable(self):
        selectionModelInstance = self.mapLevelsTable.model()
        if selectionModelInstance is not None:
            selectionModelInstance.removeRows(0, selectionModelInstance.rowCount())
    
    def _adjustTableHeight(self, mainWindow:QMainWindow):
        MARGIN_HEIGHT = 2        
        maxHeight = self._calculateAvailableSpaceForTable(mainWindow)

        totalTableHeight = self.mapLevelsTable.horizontalHeader().height()
        for row in range(self.mapLevelsTable.rowCount()):
            rowHeight = self.mapLevelsTable.rowHeight(row)
            if totalTableHeight + rowHeight > maxHeight + MARGIN_HEIGHT:
                break
            totalTableHeight += self.mapLevelsTable.rowHeight(row)
        self.mapLevelsTable.setFixedHeight(totalTableHeight + MARGIN_HEIGHT)

    def _calculateAvailableSpaceForTable(self, mainWindow:QMainWindow) -> int:
        tableCoords = self.mapLevelsTable.geometry()
        playButtonCoords = mainWindow.playMusicButton.geometry()
        return playButtonCoords.y() - tableCoords.y()
    
    def resizeLabels(self):
        labels = [self.mapTitleLabel, self.mapAuthorLabel, self.mapMapperLabel, self.mapBPMLabel, self.mapLengthLabel, 
                  self.mapRankedStateLabel, self.mapUploadedLabel, self.mapTagsLabel]
        for label in labels:
            text = label.toolTip()
            self._elideLabel(label, text)
    
    def _elideLabel(self, label:QLabel, text:str):
        label.setToolTip(text)
        labelWidth = label.width()
        fontMetrics = label.fontMetrics()

        if labelWidth > 50:
            elidedText = fontMetrics.elidedText(text, Qt.ElideRight, labelWidth)
        else:
            elidedText = "..."

        label.setText(elidedText)