from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

import os, sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uiFilePath = os.path.join(os.getcwd(), 'ui', 'main.ui')
        uic.loadUi(uiFilePath, self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindowInstance = MainWindow()
    mainWindowInstance.show()
    sys.exit(app.exec_())
