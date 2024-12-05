from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

class LabelWrapper:
    def __init__(self, label:QLabel):
        self._originalLabel = label

    def __getattr__(self, name):
        return getattr(self._originalLabel, name)
    
    def setText(self, text:str):
        MAX_LABEL_WIDTH = 50

        self._originalLabel.setToolTip(text)
        labelWidth = self._originalLabel.width()
        fontMetrics = self._originalLabel.fontMetrics()
        elidedText = fontMetrics.elidedText(text, Qt.ElideRight, labelWidth) if labelWidth > MAX_LABEL_WIDTH else '...'
        self._originalLabel.setText(elidedText)
    
    def resize(self):
        text = self._originalLabel.toolTip()
        self.setText(text)
    