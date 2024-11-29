import sys, os, base64
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QByteArray, QBuffer

from PyQt5 import uic


class PlaylistDataDialog(QDialog):
    def __init__(self, title:str='', author:str='', imageBase64String:str=''):
        super().__init__()
        uiFilePath = os.path.join(os.getcwd(), 'ui', 'playlistHeaderDialog.ui')
        uic.loadUi(uiFilePath, self)

        self.titleEdit.setText(title)
        self.authorEdit.setText(author)
        self._setImage(imageBase64String)
    
    def _setImage(self, imageBase64String:str):
        pixmap = QPixmap()

        try:
            imageData = base64.b64decode(imageBase64String)
            byteArray = QByteArray(imageData)
            isImageValid = pixmap.loadFromData(byteArray)
            if not isImageValid:
                raise Exception
        except Exception:
            return
        
        self.imageLabel.setPixmap(pixmap)
    
    def loadImage(self):
        pass

    def confirmChanges(self):
        pass

    def discardChanges(self):
        pass

    def getData(self):
        pass
    
if __name__ == "__main__":
    title = 'title'
    author = 'author'
    imageBase64String = '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'
    
    app = QApplication(sys.argv)
    window = PlaylistDataDialog(title, author, imageBase64String)
    window.show()
    sys.exit(app.exec_())