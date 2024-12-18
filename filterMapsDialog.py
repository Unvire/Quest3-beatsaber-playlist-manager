import sys, os
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel
from PyQt5 import uic

from beatSaberMap import BeatSaberMap


class FilterMapsDialog(QDialog):
    def __init__(self, mapsCacheList:list[dict]):
        super().__init__()
        uiFilePath = os.path.join(os.getcwd(), 'ui', 'searchMapsDialog.ui')
        uic.loadUi(uiFilePath, self)

        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)


if __name__ == '__main__':
    items = [{}, {}]
    app = QApplication(sys.argv)
    window = FilterMapsDialog(items)
    window.show()
    sys.exit(app.exec_())