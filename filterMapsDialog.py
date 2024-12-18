import sys, os
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit
from PyQt5 import uic

from beatSaberMap import BeatSaberMap


class FilterMapsDialog(QDialog):
    def __init__(self, mapsCacheList:list[dict]):
        super().__init__()
        uiFilePath = os.path.join(os.getcwd(), 'ui', 'searchMapsDialog.ui')
        uic.loadUi(uiFilePath, self)

        self.lengthEdit.editingFinished.connect(lambda: self._validateEdit(self.lengthEdit, 'numeric'))
        self.bpmEdit.editingFinished.connect(lambda: self._validateEdit(self.bpmEdit, 'numeric'))
        self.npsEdit.editingFinished.connect(lambda: self._validateEdit(self.npsEdit, 'numeric'))
        self.njsEdit.editingFinished.connect(lambda: self._validateEdit(self.njsEdit, 'numeric'))
        self.starsEdit.editingFinished.connect(lambda: self._validateEdit(self.starsEdit, 'numericOrStr'))
        self.uploadedEdit.editingFinished.connect(lambda: self._validateEdit(self.uploadedEdit, 'date'))

        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
    
    def _validateEdit(self, editHandle:QLineEdit, editType:str):
        print(editHandle.text(), editType)


if __name__ == '__main__':
    items = [{}, {}]
    app = QApplication(sys.argv)
    window = FilterMapsDialog(items)
    window.show()
    sys.exit(app.exec_())