from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag

class TableWidgetWrapper:
    def __init__(self, tableWidget:QTableWidget):
        self._originalTableWidget = tableWidget
    
    def __getattr__(self, name):
        return getattr(self._originalTableWidget, name)
    
    def setMode(self, mode:str):
        pass

    def _setSourceMode(self, startDragFunction, onclickFunction):
        self._originalTableWidget.setDragEnabled(True)
        self._originalTableWidget.setDragDropMode(QTableWidget.DragOnly)
        self._originalTableWidget.startDrag = startDragFunction
        self._originalTableWidget.cellClicked.connect(onclickFunction)
    
    def _setTargetMode(self, dragEnterFunction, dragMoveFunction, dropFunction, onclickFunction):
        self._originalTableWidget.setAcceptDrops(True)
        self._originalTableWidget.setDragDropMode(QTableWidget.DropOnly)
        self._originalTableWidget.dragEnterEvent = dragEnterFunction
        self._originalTableWidget.dragMoveEvent = dragMoveFunction
        self._originalTableWidget.dropEvent = dropFunction
        self._originalTableWidget.cellClicked.connect(onclickFunction)
    
    def getSelectedRows(self) -> list[int]:
        selectedRows = {index.row() for index in self._originalTableWidget.selectionModel().selectedIndexes()}
        return list(selectedRows)