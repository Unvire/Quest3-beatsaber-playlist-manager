from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from PyQt5.QtCore import Qt, QMimeData, QItemSelectionModel, QTimer
from PyQt5.QtGui import QDrag, QColor

from beatSaberPlaylist import BeatSaberPlaylist
from beatSaberMap import BeatSaberMap

class TableWidgetWrapper:
    def __init__(self, tableWidget:QTableWidget, playlistInstance:BeatSaberPlaylist, generateMapDetailsMethodHandle):
        self._originalTableWidget = tableWidget
        self.playlistInstance = playlistInstance        
        self.generateMapDetailsMethodHandle = generateMapDetailsMethodHandle
        self.hiddenRows = []

        self._originalTableWidget.cellClicked.connect(self._cellClicked)
    
    def __getattr__(self, name):
        return getattr(self._originalTableWidget, name)

    def appendRow(self, mapInstance:BeatSaberMap):
        lastRowID = self._originalTableWidget.rowCount()
        self._originalTableWidget.insertRow(lastRowID)
        newRow = QTableWidgetItem(f'{mapInstance.title} by {mapInstance.author}')
        self._originalTableWidget.setItem(lastRowID, 0, newRow)
    
    def generateRows(self):
        self.clear()
        for mapInstance in self.playlistInstance:
            self.appendRow(mapInstance)
    
    def selectRows(self, indexes:list[int]):
        selectionModelInstance = self._originalTableWidget.selectionModel()
        for index in indexes:
            selectionModelInstance.select(self._originalTableWidget.model().index(index, 0), QItemSelectionModel.Rows | QItemSelectionModel.Select)
    
    def getSelectedRows(self) -> list[int]:
        selectedRows = {index.row() for index in self._originalTableWidget.selectionModel().selectedIndexes()}
        return list(selectedRows)

    def clear(self):
        selectionModelInstance = self._originalTableWidget.model()
        if selectionModelInstance is not None:
            selectionModelInstance.removeRows(0, selectionModelInstance.rowCount())

    def unselectAll(self):
        self._originalTableWidget.selectionModel().clearSelection()
    
    def hideRows(self, indexes:list[int]):
        self.hiddenRows = indexes[:]
        for i in self.hiddenRows:
            self._showHideRow(i, True)
    
    def showAllRows(self):
        for i in self.hiddenRows:
            self._showHideRow(i, False)
    
    def scrollAndHighlightRow(self, i:int):
        self.scrollToRow(i)
        self.highlightRow(i)
    
    def scrollToRow(self, i:int):
        item = self._originalTableWidget.item(i, 0)
        self._originalTableWidget.scrollToItem(item)
    
    def highlightRow(self, i:int):
        GREEN = QColor(144, 238, 144)
        DEFAULT = Qt.white
        TIME_MS = 1000

        self._setRowBackgroundColor(i, DEFAULT)
        self._setRowBackgroundColor(i, GREEN)
        QTimer.singleShot(TIME_MS, lambda: self._setRowBackgroundColor(i, DEFAULT))
    
    def _setRowBackgroundColor(self, i:int, color:QColor):
        numOfColumns = self._originalTableWidget.columnCount()
        for col in range(numOfColumns):
            item = self._originalTableWidget.item(i, col)
            item.setBackground(color)

    def _showHideRow(self, i:int, isHide:bool):
        self._originalTableWidget.setRowHidden(i, isHide)
    
    def _cellClicked(self, row, col):
        selectedRowsList = self.getSelectedRows()
        if len(selectedRowsList) == 1:
            index = selectedRowsList[0]
            mapInstance = self.playlistInstance[index]
            self.generateMapDetailsMethodHandle(mapInstance)

class QuestSongsTable(TableWidgetWrapper):
    def __init__(self, tableWidget:QTableWidget, playlistInstance:BeatSaberPlaylist, generateMapDetailsMethodHandle):
        super().__init__(tableWidget, playlistInstance, generateMapDetailsMethodHandle)
        self._originalTableWidget.setDragEnabled(True)
        self._originalTableWidget.setDragDropMode(QTableWidget.DragOnly)
        self._originalTableWidget.startDrag = self._startDrag
    
    def _startDrag(self, supportedActions):
        drag = QDrag(self._originalTableWidget)
        mimeData = QMimeData()
        selectedRow = self._originalTableWidget.currentRow()
        
        mimeData.setText(f'{selectedRow}')
        drag.setMimeData(mimeData)
        drag.exec_(Qt.CopyAction)


class PlaylistSongsTable(TableWidgetWrapper):
    def __init__(self, tableWidget:QTableWidget, playlistInstance:BeatSaberPlaylist, generateMapDetailsMethodHandle):
        super().__init__(tableWidget, playlistInstance, generateMapDetailsMethodHandle)
        self._originalTableWidget.setAcceptDrops(True)
        self._originalTableWidget.setDragDropMode(QTableWidget.DropOnly)
        self._originalTableWidget.dragMoveEvent = self._dragMoveEvent
        self._originalTableWidget.dragEnterEvent = self._dragEnterEvent
        self._originalTableWidget.dropEvent = self._dropEvent
    
    def setSourcePlaylist(self, playlistInstance:BeatSaberPlaylist):
        self.sourcePlaylistInstance = playlistInstance

    def moveSelectedMapsUp(self):
        moveFunctionHandle = self.playlistInstance.moveSelectedItemsUp
        self._moveSelectedRowsUpDown(moveFunctionHandle)
    
    def moveSelectedMapsDown(self):
        moveFunctionHandle = self.playlistInstance.moveSelectedItemsDown
        self._moveSelectedRowsUpDown(moveFunctionHandle)

    def deleteSelectedMaps(self):
        selectedRowsList = self.getSelectedRows()
        self.playlistInstance.setSelectedIndexes(selectedRowsList)
        self.playlistInstance.removeSelectedSongs()
        self.generateRows()
    
    def _moveSelectedRowsUpDown(self, moveFunctionHandle):
        selectedRowsList = self.getSelectedRows()
        self.playlistInstance.setSelectedIndexes(selectedRowsList)
        moveFunctionHandle() #execute move up or down

        indexes = self.playlistInstance.getSelectedIndexes()
        self.generateRows()
        self.selectRows(indexes)

    def _dragMoveEvent(self, event):
        event.accept()
    
    def _dragEnterEvent(self, event):
        event.accept()
    
    def _dropEvent(self, event):
        mapIndex = int(event.mimeData().text())
        mapInstance = self.sourcePlaylistInstance[mapIndex]
        isMapAdded = self.playlistInstance.addSongIfNotPresent(mapInstance)
        if isMapAdded:
            self.appendRow(mapInstance)
        else:
            mapID = mapInstance.id
            index = self.playlistInstance.getListIndexFromMapID(mapID)
            self.scrollAndHighlightRow(index)    
        event.accept()
    
    def _cellClicked(self, row, col):
        super()._cellClicked(row, col)
        selectedRowsList = self.getSelectedRows()
        self.playlistInstance.setSelectedIndexes(selectedRowsList)