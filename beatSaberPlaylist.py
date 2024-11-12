import beatSaberMap
import bisect

class BeatSaberPlaylist:
    def __init__(self):
        self.playlistTitle = ''
        self.playlistAuthor = ''
        self.imageString = ''
        self.songsList = []

        self._selectedIndexes = []
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
        if 0 <= index < len(self.songsList) and index not in self._selectedIndexes:
            bisect.insort(self._selectedIndexes, index)

    def unselect(self, index:int):
        if index in self._selectedIndexes:
            self._selectedIndexes.remove(index)

    def moveSelectedItemsUp(self):
        pass

    def moveSelectedItemsDown(self):
        pass

    def _unselectedIndexes(self):
        numberOfSongs = len(self.songsList)
        return [i for i, _ in enumerate(range(numberOfSongs)) if i not in self._selectedIndexes]


if __name__ == '__main__':
    a = BeatSaberPlaylist()