import beatSaberMap
import bisect, json

class BeatSaberPlaylist:
    def __init__(self):
        self.playlistTitle = ''
        self.playlistAuthor = ''
        self.imageString = ''
        self.songsList = []

        self._selectedIndexes = []
        self._selectionGroups = []

    def loadFromFile(self, filePath:str):
        fileContent = ''
        with open(filePath, 'r') as file:
            fileContent = ''.join(file.readlines())
        
        if not fileContent:
            return
        
        playlistJSON = json.loads(fileContent)
        playlistTitle = playlistJSON.get('playlistTitle', '')
        playlistAuthor = playlistJSON.get('playlistAuthor', '')
        playlistImage = playlistJSON.get('image', '')
        playlistSongs = playlistJSON.get('songs', '')

        self.setPlaylistTitle(playlistTitle)
        self.setPlaylistAuthor(playlistAuthor)
        self.setImageString(playlistImage)
        self._createSongsListFromJSON(playlistSongs)
    
    def _createSongsListFromJSON(self, songsListJSON:list[dict]):
        for songJSON in songsListJSON:
            songID = songJSON['key']
            beatSaberMapInstance = beatSaberMap.BeatSaberMap(songID)
            beatSaberMapInstance.getDataFromBeatSaverApi()
            self.addSong(beatSaberMapInstance)

    def saveToFile(self, filePath:str):
        serializedInstance = self.serializeInstanceToJSON()
        with open(filePath, 'w') as file:
            file.write(serializedInstance)

    def serializeInstanceToJSON(self) -> str:
        result = {}
        result['playlistTitle'] = self.getPlaylistTitle()
        result['playlistAuthor'] = self.getPlaylistAuthor()
        result['image'] = self.getImageString()
        result['songs'] = [beatSaberMapInstance.generateDictForPlaylist() for beatSaberMapInstance in self.songsList]
        return json.dumps(result, indent=4)

    def setPlaylistTitle(self, title:str):
        self.playlistTitle = title
    
    def getPlaylistTitle(self) -> str:
        return self.playlistTitle
    
    def setPlaylistAuthor(self, author:str):
        self.playlistAuthor = author
    
    def getPlaylistAuthor(self) -> str:
        return self.playlistAuthor
    
    def setImageString(self, imageString:str):
        self.imageString = imageString
    
    def getImageString(self):
        return self.imageString

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
    def openFile() -> str:        
        from tkinter import filedialog
        filePath = filedialog.askopenfile(mode='r', filetypes=[('*', '*')])
        return filePath.name
    
    filePath = openFile()
    a = BeatSaberPlaylist()
    a.loadFromFile(filePath)    
    print('Loaded playlist:\n', a.serializeInstanceToJSON())
    a.select(1)
    a.moveSelectedItemsUp()
    a.unselect(0) # index=1 became index=0 after moving up
    print('\nOrder changed playlist:\n', a.serializeInstanceToJSON())
    a.select(2)
    a.removeSelectedSongs()
    print('\nSong removed:\n', a.serializeInstanceToJSON())