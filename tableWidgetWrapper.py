from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag

from beatSaberPlaylist import BeatSaberPlaylist
from beatSaberMap import BeatSaberMap

class TableWidgetWrapper:
    def __init__(self, tableWidget:QTableWidget, playlistInstance:BeatSaberPlaylist, gui):
        self._originalTableWidget = tableWidget
        self.playlistInstance = playlistInstance        
        self.gui = gui
    
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
    
    def getSelectedRows(self) -> list[int]:
        selectedRows = {index.row() for index in self._originalTableWidget.selectionModel().selectedIndexes()}
        return list(selectedRows)

    def clear(self):
        selectionModelInstance = self._originalTableWidget.model()
        if selectionModelInstance is not None:
            selectionModelInstance.removeRows(0, selectionModelInstance.rowCount())

    def unselectAll(self):
        self._originalTableWidget.selectionModel().clearSelection()

class QuestSongsTable(TableWidgetWrapper):
    def __init__(self, tableWidget:QTableWidget, playlistInstance:BeatSaberPlaylist, gui):
        super().__init__(tableWidget, playlistInstance, gui)
        self._originalTableWidget.setDragEnabled(True)
        self._originalTableWidget.setDragDropMode(QTableWidget.DragOnly)
        self._originalTableWidget.startDrag = self._startDrag
        self._originalTableWidget.cellClicked.connect(self._cellClicked)
    
    def _startDrag(self, supportedActions):
        drag = QDrag(self._originalTableWidget)
        mimeData = QMimeData()
        selectedRow = self._originalTableWidget.currentRow()
        
        mimeData.setText(f'{selectedRow}')
        drag.setMimeData(mimeData)
        drag.exec_(Qt.CopyAction)

    def _cellClicked(self, row, col):
        selectedRowsList = self.getSelectedRows()
        if selectedRowsList:
            row = selectedRowsList[0]
            mapInstance = self.playlistInstance[row]
            self.gui.generateMapDetails(mapInstance)


class PlaylistSongsTable(TableWidgetWrapper):
    def __init__(self, tableWidget:QTableWidget, playlistInstance:BeatSaberPlaylist, gui):
        super().__init__(tableWidget, playlistInstance, gui)
        self._originalTableWidget.setAcceptDrops(True)
        self._originalTableWidget.setDragDropMode(QTableWidget.DropOnly)
        self._originalTableWidget.dragMoveEvent = self._dragMoveEvent
        self._originalTableWidget.dragEnterEvent = self._dragEnterEvent
        self._originalTableWidget.dropEvent = self._dropEvent
        self._originalTableWidget.cellClicked.connect(self._cellClicked)
    
    def setSourcePlaylist(self, playlistInstance:BeatSaberPlaylist):
        self.sourcePlaylistInstance = playlistInstance

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
        event.accept()
    
    def _cellClicked(self, row, col):
        selectedRowsList = self.getSelectedRows()
        if len(selectedRowsList) == 1:
            index = selectedRowsList[0]
            mapInstance = self.playlistInstance[index]
            self.gui.generateMapDetails(mapInstance)

        self.playlistInstance.setSelectedIndexes(selectedRowsList)