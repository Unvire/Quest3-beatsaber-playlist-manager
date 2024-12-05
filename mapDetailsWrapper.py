from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QMainWindow, QHeaderView

from beatSaberMap import BeatSaberMap
from labelWrapper import LabelWrapper

class MapDetailsWrapper:
    def __init__(self):
        self.webRequestDetails = None
        self.staticDetails = None
        self.firstWidgetBelowTable = None

    def setStaticWidgets(self, authorLabel:LabelWrapper, titleLabel:LabelWrapper, mapperLabel:LabelWrapper, 
                         bpmLabel:LabelWrapper, lengthTimeLabel:LabelWrapper, rankedStateLabel:LabelWrapper, 
                         uploadedLabel:LabelWrapper, mapTagsLabel:LabelWrapper, levelsTable:QTableWidget):
        self.staticDetails = StaticDetails(authorLabel, titleLabel, mapperLabel, bpmLabel, lengthTimeLabel, 
                 rankedStateLabel, uploadedLabel, mapTagsLabel, levelsTable)
    
    def setFirstWidgetBelowTable(self, widget:QWidget):
        self.firstWidgetBelowTable = widget

    def update(self, mapInstance:BeatSaberMap):
        self.staticDetails.setFirstWidgetBelowTable(self.firstWidgetBelowTable)
        self.staticDetails.update(mapInstance)
    
    def resize(self):
        self.staticDetails.resize()


class WebRequestMapDetails:
    pass


class StaticDetails:
    def __init__(self, authorLabel:LabelWrapper, titleLabel:LabelWrapper, mapperLabel:LabelWrapper, 
                 bpmLabel:LabelWrapper, lengthTimeLabel:LabelWrapper, rankedStateLabel:LabelWrapper, 
                 uploadedLabel:LabelWrapper, mapTagsLabel:LabelWrapper, levelsTable:QTableWidget):
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

        self.firstWidgetBelowTable = None
    
    def setFirstWidgetBelowTable(self, widget:QWidget):
        self.firstWidgetBelowTable = widget
    
    def update(self, mapInstance:BeatSaberMap):
        lengthTime = self._formatSeconds(mapInstance.lengthSeconds)
        tags = ", ".join(mapInstance.tagsList)
        self._updateLabels(author=mapInstance.author, title=mapInstance.title, mapper=mapInstance.mapper, 
                           bpm=mapInstance.bpm, lengthTime=lengthTime, rankedState=mapInstance.rankedState, 
                           uploaded=mapInstance.uploaded, tags=tags)
        self._updateTable(mapInstance)

    def resize(self):
        labels = [self.mapAuthorLabel, self.mapTitleLabel, self.mapMapperLabel, self.mapBPMLabel, 
                        self.mapLengthLabel, self.mapRankedStateLabel, self.mapUploadedLabel, 
                        self.mapTagsLabel]
            
        for label in labels:
            label.resize()
    
    def _formatSeconds(self, lengthSeconds:int) -> str:
        minutes, seconds = divmod(lengthSeconds, 60)
        seconds = f'0{seconds}' if seconds < 10 else seconds
        return f'{minutes}:{seconds}'

    def _updateLabels(self, author:str='', title:str='', mapper:str='',bpm:str='', lengthTime:str='', 
                      rankedState:str='',uploaded:str='', tags:str=''):
        self.mapAuthorLabel.setText(f'Author: {author}')
        self.mapTitleLabel.setText(f'Title: {title}')
        self.mapMapperLabel.setText(f'Mapper: {mapper}')
        self.mapBPMLabel.setText(f'BPM: {bpm}')
        self.mapLengthLabel.setText(f'Length: {lengthTime}')
        self.mapRankedStateLabel.setText(f'Ranked state: {rankedState}')
        self.mapUploadedLabel.setText(f'Uploaded: {uploaded}')
        self.mapTagsLabel.setText(f'Tags: {tags}')
    
    def _updateTable(self, mapInstance:BeatSaberMap):
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
        self._adjustTableHeight()
    
    def _clearTable(self):
        selectionModelInstance = self.mapLevelsTable.model()
        if selectionModelInstance is not None:
            selectionModelInstance.removeRows(0, selectionModelInstance.rowCount())
    
    def _adjustTableHeight(self):
        MARGIN_HEIGHT = 2        
        maxHeight = self._calculateAvailableSpaceForTable()

        totalTableHeight = self.mapLevelsTable.horizontalHeader().height()
        for row in range(self.mapLevelsTable.rowCount()):
            rowHeight = self.mapLevelsTable.rowHeight(row)
            if totalTableHeight + rowHeight > maxHeight + MARGIN_HEIGHT:
                break
            totalTableHeight += self.mapLevelsTable.rowHeight(row)
        self.mapLevelsTable.setFixedHeight(totalTableHeight + MARGIN_HEIGHT)

    def _calculateAvailableSpaceForTable(self) -> int:
        tableCoords = self.mapLevelsTable.geometry()
        widgetCoords = self.firstWidgetBelowTable.geometry()
        return widgetCoords.y() - tableCoords.y()