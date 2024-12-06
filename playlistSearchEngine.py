from beatSaberPlaylist import BeatSaberPlaylist
from beatSaberMap import BeatSaberMap

import re

class SearchEngine:
    def __init__(self):
        self.cache = {}
        self.keywords = set(['__length', '__bpm', '__mods', '__nps', '__njs', '__uploaded', '__stars', '__state'])

    def cachePlaylistData(self, playlistInstance:BeatSaberPlaylist):
        for i, map in enumerate(playlistInstance):
            mapCache = self.cacheMapData(map)
            self.cache[i] = mapCache
    
    def cacheMapData(self, mapInstance:BeatSaberMap):        
        diffLongString = ''.join([f'{level.difficulty}{level.characteristic}' for level in mapInstance.getDiffs()])
        longString = f'{mapInstance.title}{mapInstance.author}{mapInstance.mapper}' + diffLongString + ''.join(mapInstance.tagsList)
        longString = longString.replace(' ', '')

        cacheDict = {
            'longString': longString,
            '__length': mapInstance.lengthSeconds,
            '__bpm': mapInstance.bpm,
            '__mods': mapInstance.getRequiredMods(),
            '__nps': mapInstance.getNpsRange(),
            '__njs': mapInstance.getNjsRange(),
            '__uploaded': mapInstance.uploaded,
            '__stars': mapInstance.getStarsRange(),
            '__state': mapInstance.rankedState,
        }
        return cacheDict
    
    def filterMaps(self, searchRequestString:str) -> list[int]:
        words = searchRequestString.split(' ')
        keywordsInRequest = self.keywords & set(words)
        regexSearchWords = set(words) - keywordsInRequest

        matchingLongStringIndexes = self._checkLongstrings(regexSearchWords)

    def _checkLongstrings(self, regexSearchWords:str) -> list[int]:
        result = []
        for i, cacheDict in enumerate(self.cache):
            isMatch = True
            for word in regexSearchWords:
                if re.search(word, cacheDict['longString']):
                    isMatch = False
                    break
            if isMatch:
                result.append(i)
        return i

    def _checkKeywords(self, keywords:list[str]) -> list[int]:
        pass