from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QWidget, QTableWidgetItem
from PyQt5 import uic

import os, sys
from beatSaverAPICaller import BeatSaverAPICaller
from beatSaberPlaylist import BeatSaberPlaylist
from beatSaberMap import BeatSaberMap

class MainWindow(QMainWindow):
    def __init__(self):
        self.allMapsList = []

        super().__init__()
        uiFilePath = os.path.join(os.getcwd(), 'ui', 'main.ui')
        uic.loadUi(uiFilePath, self)

        for table in (self.playlistsMapsTable, self.allMapsTable):
            header = table.horizontalHeader()  
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(1, QHeaderView.Stretch)
        
        self.actionConnect.triggered.connect(self.getSongsFromQuest)
    
    def getSongsFromQuest(self) -> dict:
        responseJSON = self.__mockGetSongsFromQuest()
        for key, mapJSON in responseJSON.items():
            BeatSaberMapInstance = BeatSaberMap(key)
            BeatSaberMapInstance.getDataFromBeatSaverJSON(mapJSON)
            self.allMapsList.append(BeatSaberMapInstance)
        
        self.updateTable(self.allMapsTable, self.allMapsList)

    def __mockGetSongsFromQuest(self) -> dict:
        mapsIDsPath = os.path.join(os.getcwd(), 'other', 'ls_questSongs.txt')
        with open(mapsIDsPath, 'r', encoding='utf-8') as file:
            buffer = file.readlines()
        songsIDsList = [line.split('\\')[0] for line in buffer]
        return BeatSaverAPICaller.multipleMapsCall(songsIDsList)
    
    def updateTable(self, table:QWidget, mapsList:list[BeatSaberMap]):
        for i, map in enumerate(mapsList):
            table.insertRow(i)
            table.setItem(i, 0, QTableWidgetItem(f'{map.name}'))
            table.setItem(i, 1, QTableWidgetItem(f'a'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindowInstance = MainWindow()
    mainWindowInstance.show()

    
    sys.exit(app.exec_())
