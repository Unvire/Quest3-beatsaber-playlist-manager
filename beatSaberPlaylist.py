import beatSaberMap, beatSaverAPICaller
import bisect, json

class BeatSaberPlaylist:
    def __init__(self):
        self.playlistTitle = ''
        self.playlistAuthor = ''
        self.imageString = ''
        self.songsList = []

        self._selectedIndexes = []
        self._selectionGroups = []

        self._isSortingReversed = False
        self._idSet = set()

    def __repr__(self):
        return self.serializeInstanceToJSON()

    def __iter__(self):
        return iter(self.songsList)
    
    def __getitem__(self, index):
        return self.songsList[index]

    def loadFromFile(self, filePath:str) -> bool:
        self._clearPlaylist()
        
        fileContent = ''
        with open(filePath, 'r', encoding='utf-8') as file:
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
        try:
            self._createSongsListFromJSON(playlistSongs)
        except Exception:
            return False
        return True
    
    def _clearPlaylist(self):
        self.__init__()
    
    def _createSongsListFromJSON(self, songsListJSON:list[dict]):        
        apiCaller = beatSaverAPICaller.BeatSaverAPICaller

        songIDList = [songJSON['key'] for songJSON in songsListJSON]
        responseJSON = apiCaller.multipleMapsCall(songIDList)
        for key, mapJSON in responseJSON.items():
            self._addMapFromJSON(key, mapJSON)

    def serializeInstanceToJSON(self) -> str:
        result = {
            'playlistTitle': self.getPlaylistTitle(),
            'playlistAuthor': self.getPlaylistAuthor(),
            'image': self.getImageString(),
            'songs': [beatSaberMapInstance.generateDictForPlaylist() for beatSaberMapInstance in self.songsList]
        }
        return json.dumps(result, indent=4)
    
    def generateFromResponseDict(self, playlistJSON:dict):
        for key, mapJSON in playlistJSON.items():
            self._addMapFromJSON(key, mapJSON)
    
    def _addMapFromJSON(self, key:str, mapJSON:dict):
        BeatSaberMapInstance = beatSaberMap.BeatSaberMap(key)
        BeatSaberMapInstance.getDataFromBeatSaverJSON(mapJSON)
        self.addSongIfNotPresent(BeatSaberMapInstance)

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

    def addSongIfNotPresent(self, newSong:beatSaberMap.BeatSaberMap) -> bool:
        isAdded = False
        if newSong.id not in self._idSet:
            self.songsList.append(newSong)
            self._idSet.add(newSong.id)
            isAdded = True

        return isAdded
    
    def getSongsByIds(self, mapIdsList:list[str]) -> list[beatSaberMap.BeatSaberMap]:
        result = []
        numOfSongs = len(mapIdsList)
        for song in self.songsList:
            if song.id in mapIdsList:
                result.append(song)
                numOfSongs -= 1
            if numOfSongs <= 0:
                break
        return result

    def removeSelectedSongs(self):
        while self._selectedIndexes:
            currentIndex = self._selectedIndexes.pop()
            song = self.songsList[currentIndex]
            self._idSet.remove(song.id)
            self.songsList.pop(currentIndex)
    
    def select(self, index:int):
        if 0 <= index < len(self.songsList) and index not in self._selectedIndexes:
            bisect.insort(self._selectedIndexes, index)

    def unselect(self, index:int):
        if index in self._selectedIndexes:
            self._selectedIndexes.remove(index)
    
    def setSelectedIndexes(self, indexesList:list[int]):
        self._selectedIndexes = indexesList
    
    def getSelectedIndexes(self) -> list[int]:
        return self._selectedIndexes[:]
    
    def getSongsIds(self) -> list[str]:
        return list(self._idSet)
    
    def checkMissingSongs(self, targetPlaylist:'BeatSaberPlaylist') -> list[str]:
        targetIndexes = set(targetPlaylist.getSongsIds())
        return list(targetIndexes - self._idSet)

    def moveSelectedItemsUp(self):
        newSongsOrder = self._calculateSongIndexesAfterMoveUp()
        songsAfterReordering = self._reorderSongs(newSongsOrder)
        selectionIndexesAfterReordering = self._caluclateSelectedIndexesAfterMoveUp()
        
        self.songsList = songsAfterReordering
        self._selectedIndexes = selectionIndexesAfterReordering
    
    def sortPlaylistInPlaceBy(self, order:str):
        sortingOrderKeysDict = {
            'Upload date': lambda mapInstance: mapInstance.uploaded,
            'Title': lambda mapInstance: mapInstance.title.lower(),
            'Author': lambda mapInstance: mapInstance.author.lower(),
            'BPM': lambda mapInstance: mapInstance.bpm,
            'Ranked state': lambda mapInstance: mapInstance.rankedState,
            'Mapper': lambda mapInstance: mapInstance.mapper.lower(),
        }

        if order in sortingOrderKeysDict:
            sortingKey = sortingOrderKeysDict[order]
            self.songsList = sorted(self.songsList, reverse=self._isSortingReversed, key=sortingKey)

    def resetSortingReverseMode(self):
        self._isSortingReversed = False
        
    def changeSortingOrder(self):
        self._isSortingReversed = not self._isSortingReversed
    
    def isEmpty(self) -> bool:
        return len(self.songsList) == 0

    def getListIndexFromMapID(self, mapID:str) -> int:
        for i, song in enumerate(self.songsList):
            if mapID == song.id:
                return i
    
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

    print('Iteration over playlist')
    for song in a:
        print(song)
    print('Accessing element by index')
    print(a[1])

    print('Loaded playlist:\n', a.serializeInstanceToJSON())
    a.select(1)
    a.moveSelectedItemsUp()
    a.unselect(0) # index=1 became index=0 after moving up
    print('\nOrder changed playlist:\n', a.serializeInstanceToJSON())
    a.select(2)
    a.removeSelectedSongs()
    print('\nSong removed:\n', a) # a.__repr__ calls a.serializeInstanceToJSON()