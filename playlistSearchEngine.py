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
        cacheDict = {
            'longString': self._buildLongString(mapInstance),
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

    def _buildLongString(self, mapInstance:BeatSaberMap) -> str:
        words = set()
        words.add(mapInstance.title)
        words.add(mapInstance.author)
        words.add(mapInstance.mapper)

        for level in mapInstance.getDiffs():
            words.add(level.difficulty)
            words.add(level.characteristic)
        
        for tag in mapInstance.tagsList:
            words.add(tag)
        return ' '.join(list(words))        
    
    def filterMaps(self, searchRequestString:str) -> list[int]:
        if not searchRequestString:
            return [i for i in range(len(self.cache))]
        
        words = searchRequestString.split(' ')
        regexSearchWords = words[0] if words[0].startswith('__') else None
        keywords = self._findKeywords(words)

        if regexSearchWords:
            matchingLongStringIndexes = self._checkLongstrings(regexSearchWords)
        if keywords:
            matchingKeywordsIndexes = self._checkKeywords(keywords)

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
    
    def _findKeywords(self, words:list[str]) -> list[list[str, str]]:
        keywords = []
        for word in words:
            subWords = word.split('=')
            if len(subWords) != 2:
                continue

            if not subWords[0] in self.keywords:
                continue
            
            keyword, criteria = subWords
            keywords.append([keyword, criteria])
        return keywords

    def _checkKeywords(self, keywords:list[list[str, str]]) -> list[int]:
        rangeKeywords = ['__length', '__bpm',  '__nps', '__njs', '__stars']
        stringKeywords = ['__mods', '__state', '__stars']
        result = []
        for keyword, criteria in keywords:
            for i, cacheDict in enumerate(self.cache):
                if keyword in rangeKeywords:
                    isInRange = self._checkIfInRange(self, criteria, cacheDict[keyword])
                    if isInRange:
                        result.append(i)
                        
                if keyword in stringKeywords:
                    pass
    
    def _checkIfInRange(self, criteria:str, value:float|int) -> bool:
        rangePattern = '\[(-?\d*(?:\.\d+)?)?\s*;\s*(-?\d*(?:\.\d+)?)?]' # checks if criteria is 2 numbers [1.2;2.3], 1 number [;1] or [1;] or [;]
        if not re.match(rangePattern, criteria):
            return True
        
        minValStr, maxValStr = criteria[1:-1].split(';')
        minVal = float(minValStr) if minValStr else float('-inf')
        maxVal = float(maxValStr) if maxValStr else float('inf')
        return minVal <= float(value) <= maxVal
