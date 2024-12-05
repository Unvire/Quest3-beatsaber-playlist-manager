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

        self.mapLevelsTable = MapDetailsTable(levelsTable)

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
        self.mapLevelsTable.clear()
        self.mapLevelsTable.fillRows(mapInstance, self.firstWidgetBelowTable)

        

class MapDetailsTable:
    def __init__(self, table:QTableWidget):
        self._originalTableWidget = table
        
        header = self._originalTableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
    
    def __getattr__(self, name):
        return getattr(self._originalTableWidget, name)
    
    def clear(self):
        selectionModelInstance = self._originalTableWidget.model()
        if selectionModelInstance is not None:
            selectionModelInstance.removeRows(0, selectionModelInstance.rowCount())
    
    def fillRows(self, mapInstance:BeatSaberMap, widgetBelowTable:QWidget):
        for level in mapInstance.diffs:
            iRow = self._originalTableWidget.rowCount()
            self._originalTableWidget.insertRow(iRow)
            for iCol, text in enumerate([level.difficulty, level.characteristic, level.stars, level.njs, level.nps, level.requiredMods]):
                self.fillCell(iRow, iCol, str(text))
        self._adjustTableHeight(widgetBelowTable)
    
    def fillCell(self, row:int, col:int, text:str):
        self._originalTableWidget.setItem(row, col, QTableWidgetItem(text))
    
    def _adjustTableHeight(self, widgetBelowTable:QWidget):
        MARGIN_HEIGHT = 2        
        maxHeight = self._calculateAvailableSpaceForTable(widgetBelowTable)

        totalTableHeight = self._originalTableWidget.horizontalHeader().height()
        for row in range(self._originalTableWidget.rowCount()):
            rowHeight = self._originalTableWidget.rowHeight(row)
            if totalTableHeight + rowHeight > maxHeight + MARGIN_HEIGHT:
                break
            totalTableHeight += self._originalTableWidget.rowHeight(row)
        self._originalTableWidget.setFixedHeight(totalTableHeight + MARGIN_HEIGHT)

    def _calculateAvailableSpaceForTable(self, widgetBelowTable:QWidget) -> int:
        tableCoords = self._originalTableWidget.geometry()
        widgetCoords = widgetBelowTable.geometry()
        return widgetCoords.y() - tableCoords.y()