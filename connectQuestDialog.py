import sys, os
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import uic

from adbWrapperFactory import AdbWrapperFactory

class ConnectQuestThread(QThread):
    updateLabelsSignal = pyqtSignal(int, bool)
    finishedSignal = pyqtSignal()

    MAX_RETRIES = 60

    def __init__(self, wrapperInstance: AdbWrapperFactory):
        super().__init__()
        self.wrapperInstance = wrapperInstance
        self.isThreadRunning = True
        self.isConnected = False
        
    def run(self):
        i = 1
        while not self.isConnected and i <= ConnectQuestThread.MAX_RETRIES and self.isThreadRunning:
            self.isConnected = self.wrapperInstance.isDebugModeEnabled()
            self.updateLabelsSignal.emit(i, self.isConnected)
            i += 1
            self.sleep(1)
        self.isThreadRunning = False

    def stop(self):
        self.isThreadRunning = False
        self.finishedSignal.emit()
    
    def getConnectionResult(self) -> bool:
        return self.isConnected
    


class ConnectQuestDialog(QDialog):
    def __init__(self, wrapperInstance:AdbWrapperFactory):
        super().__init__()
        uiFilePath = os.path.join(os.getcwd(), 'ui', 'connectQuestDialog.ui')
        uic.loadUi(uiFilePath, self)       
        
        self.isConnected = False
        self.wrapperInstance = wrapperInstance        

        self.workerThread = ConnectQuestThread(self.wrapperInstance)
        self.workerThread.updateLabelsSignal.connect(self._updateLabels)
        self.workerThread.finishedSignal.connect(self._threadFinished)

        self._updateLabels(0, False)
        self.backButton.clicked.connect(self.buttonPressed)
    
    def show(self):
        super().show()
        self._attemptConnection()
    
    def _attemptConnection(self):
        self.workerThread.wait()
        self.workerThread.start()

    def _threadFinished(self):
        self.isConnected = self.workerThread.getConnectionResult()
    
    def getData(self) -> bool:
        return self.isConnected

    def closeEvent(self, event):
        self.finishThreadExecution()
        super().closeEvent(event)

    def buttonPressed(self, event):
        self.finishThreadExecution()
        self.accept()
    
    def finishThreadExecution(self):
        self.workerThread.stop()
        self.workerThread.wait()
        self.deleteLater()
            
    def _updateLabels(self, iAttempt:int, isConnected:bool):
        self.attemptsLabel.setText(f'{iAttempt}/{ConnectQuestThread.MAX_RETRIES}')
        if isConnected:
            self.resultLabel.setText(f'connected')
            self.resultLabel.setStyleSheet('color: #339999;')
        else:
            self.resultLabel.setText(f'not connected')
            self.resultLabel.setStyleSheet('color: red;')
        self.attemptsLabel.repaint()
        self.resultLabel.repaint()


if __name__ == '__main__':
    wrapper = AdbWrapperFactory('windows')
    app = QApplication(sys.argv)
    window = ConnectQuestDialog(wrapper)
    window.show()
    sys.exit(app.exec_())