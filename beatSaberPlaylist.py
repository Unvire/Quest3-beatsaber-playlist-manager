import beatSaberMap

class BeatSaberPlaylist:
    def __init__(self):
        self.playlistTitle = ''
        self.playlistAuthor = ''
        self.imageString = ''
        self.songsList = []

        self._selectedIndexes = set()
        self._selectionGroups = []

    def loadFromFile(self):
        pass

    def saveToFile(self):
        pass

    def addSong(self):
        pass

    def removeSong(self):
        pass

    def select(self, index:int):
        if 0 <= index < len(self.songsList):
            self._selectedIndexes.add(index)
        
        self._selectionGroups = self._makeSelectionGroups()

    def unselect(self, index:int):
        if index in self._selectedIndexes:
            self._selectedIndexes.remove(index)
    
    def _makeSelectionGroups(self) -> list[list[int]]:
        selectedIndexesList = sorted(list(self._selectedIndexes))
        if not selectedIndexesList:
            return [[]]
        
        firstItem = selectedIndexesList.pop(0)
        group = [firstItem]
        groups = []
        for index in selectedIndexesList:
            if group[-1] == index - 1:
                group.append(index)
            else:
                groups.append(group)
                group = [index]

        groups.append(group)
        
        return groups

    def moveSelectedItemsUp(self):
        pass

    def moveSelectedItemsDown(self):
        pass


if __name__ == '__main__':
    a = BeatSaberPlaylist()