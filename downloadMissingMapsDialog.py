import sys, os
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel
from PyQt5 import uic

from beatSaberMap import BeatSaberMap


class DownloadMissingMapsDialog(QDialog):
    def __init__(self, mapsList:list[BeatSaberMap]):
        super().__init__()
        uiFilePath = os.path.join(os.getcwd(), 'ui', 'downloadMissingMapsDialog.ui')
        uic.loadUi(uiFilePath, self)        
        
        layout = QVBoxLayout(self.scrollAreaWidgetContents)    
        self.scrollAreaWidgetContents.setLayout(layout)        

        for mapInstance in mapsList:
            labelText = f'{mapInstance.title} by {mapInstance.author} [{mapInstance.id}]'
            linkLabel = QLabel(f'<a href="{mapInstance.downloadUrl}">{labelText}</a>')
            linkLabel.setOpenExternalLinks(True)
            layout.addWidget(linkLabel)
        
        self.okButton.clicked.connect(self.accept)


if __name__ == '__main__':
    def createMapMockInstance(index:int) -> BeatSaberMap:
        a = BeatSaberMap(f'{index}')
        a.downloadUrl = 'https://www.google.com'
        a.title = f'testTitle'
        a.author = f'testAuthor'
        return a
    
    items = [createMapMockInstance(i) for i in range(100)]
    app = QApplication(sys.argv)
    window = DownloadMissingMapsDialog(items)
    window.show()
    sys.exit(app.exec_())