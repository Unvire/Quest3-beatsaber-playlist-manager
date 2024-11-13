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

    def addSong(self, song:beatSaberMap.BeatSaberMap):
        self.songsList.append(song)

    def removeSelectedSongs(self):
        while self._selectedIndexes:
            currentIndex = self._selectedIndexes.pop()
            self.songsList.pop(currentIndex)
    
    def select(self, index:int):
        if 0 <= index < len(self.songsList) and index not in self._selectedIndexes:
            bisect.insort(self._selectedIndexes, index)

    def unselect(self, index:int):
        if index in self._selectedIndexes:
            self._selectedIndexes.remove(index)

    def moveSelectedItemsUp(self):
        newSongsOrder = self._calculateSongIndexesAfterMoveUp()
        songsAfterReordering = self._reorderSongs(newSongsOrder)
        selectionIndexesAfterReordering = self._caluclateSelectedIndexesAfterMoveUp()
        
        self.songsList = songsAfterReordering
        self._selectedIndexes = selectionIndexesAfterReordering
    
    def _calculateSongIndexesAfterMoveUp(self) -> list[int]:
        unselectedIndexes = self._getUnselectedIndexes()
        selectedGroups = self._makeSelectionGroups(self._selectedIndexes)
        
        newOrder = []
        while unselectedIndexes:
            unselectedIndex = unselectedIndexes.pop(0)
            if selectedGroups:
                selectedGroup = selectedGroups[0]
                if unselectedIndex + 1 == selectedGroup[0] or selectedGroup[0] == 0:
                    newOrder += selectedGroups.pop(0)
            newOrder.append(unselectedIndex)
        
        if selectedGroups:
            newOrder += selectedGroups[0]
        return newOrder
    
    def _caluclateSelectedIndexesAfterMoveUp(self) -> list[int]:
        selectedGroups = self._makeSelectionGroups(self._selectedIndexes)

        result = []
        for group in selectedGroups:
            result += [index - 1 if 0 not in group else index for index in group]
    
        return result

    def moveSelectedItemsDown(self):        
        newSongsOrder = self._calculateSongIndexesAfterMoveDown()
        songsAfterReordering = self._reorderSongs(newSongsOrder)
        
        self.songsList = songsAfterReordering
        self._selectedIndexes = self._caluclateSelectedIndexesAfterMoveDown()

    def _caluclateSelectedIndexesAfterMoveDown(self) -> list[int]:
        selectedGroups = self._makeSelectionGroups(self._selectedIndexes)

        result = []
        lastItemIndex = len(self.songsList) - 1
        for group in selectedGroups:
            result += [index + 1 if lastItemIndex not in group else index for index in group]
    
        return result

    def _calculateSongIndexesAfterMoveDown(self) -> list[int]:
        unselectedIndexes = self._getUnselectedIndexes()
        selectedGroups = self._makeSelectionGroups(self._selectedIndexes)

        newOrder = []
        while unselectedIndexes:
            unselectedIndex = unselectedIndexes.pop(0)
            newOrder.append(unselectedIndex)
            if selectedGroups:
                selectedGroup = selectedGroups[0]
                if unselectedIndex - 1 == selectedGroup[-1]:
                    newOrder += selectedGroups.pop(0)
        
        if selectedGroups:
            newOrder += selectedGroups[0]
        return newOrder

    def _reorderSongs(self, newOrder:list[int]) -> list[beatSaberMap.BeatSaberMap]:
        result = []
        while newOrder:
            currentIndex = newOrder.pop(0)
            result.append(self.songsList[currentIndex])
        return result

    def _getUnselectedIndexes(self):
        numberOfSongs = len(self.songsList)
        return [i for i, _ in enumerate(range(numberOfSongs)) if i not in self._selectedIndexes]
    
    def _makeSelectionGroups(self, selectedIndexesList:list[int]) -> list[list[int]]:
        selectedIndexesList = sorted(selectedIndexesList)
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

if __name__ == '__main__':
    a = BeatSaberPlaylist()
    a.songsList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    a._selectedIndexes = [2, 4, 5, 7]

    a.moveSelectedItemsUp()