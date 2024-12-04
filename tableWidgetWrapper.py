from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag

from beatSaberPlaylist import BeatSaberPlaylist

class TableWidgetWrapper:
    def __init__(self, tableWidget:QTableWidget):
        self._originalTableWidget = tableWidget
    
    def __getattr__(self, name):
        return getattr(self._originalTableWidget, name)
    
    def getSelectedRows(self) -> list[int]:
        selectedRows = {index.row() for index in self._originalTableWidget.selectionModel().selectedIndexes()}
        return list(selectedRows)
    

class QuestSongsTable(TableWidgetWrapper):
    def __init__(self, tableWidget:QTableWidget, playlistInstance:BeatSaberPlaylist, gui):
        super().__init__(tableWidget)
        self._originalTableWidget.setDragEnabled(True)
        self._originalTableWidget.setDragDropMode(QTableWidget.DragOnly)
        self.playlistInstance = playlistInstance
        self._originalTableWidget.startDrag = self._startDrag
        self._originalTableWidget.cellClicked.connect(self._cellClicked)

        self.gui = gui
    
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
    def __init__(self, tableWidget:QTableWidget, dragEnterFunction, dragMoveFunction, dropFunction, onclickFunction):
        super().__init__(tableWidget)
        self._originalTableWidget.setAcceptDrops(True)
        self._originalTableWidget.setDragDropMode(QTableWidget.DropOnly)
        self._originalTableWidget.dragEnterEvent = dragEnterFunction
        self._originalTableWidget.dragMoveEvent = dragMoveFunction
        self._originalTableWidget.dropEvent = dropFunction
        self._originalTableWidget.cellClicked.connect(onclickFunction)