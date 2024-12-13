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
        
        longStrings, keywords = self._findLongStringsAndKeywords(searchRequestString)
        processedKeyWords = self._processKeywords(keywords)

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
    
    def _findLongStringsAndKeywords(self, request:str) -> tuple[list[str], list[str]]:
        words = request.split(' ')
        keywords = []
        longStrings = []
        for word in words:
            if not word.startswith('__'):
                longStrings.append(word)
                continue

            potentialKeyword = word.split('=')[0]
            if not potentialKeyword in self.keywords:
                longStrings.append(word)
                continue
            keywords.append(word)
        return longStrings, keywords
    
    def _processKeywords(self, possibleKeyWords:list[str]) -> list[list[str, str] | list[str, float, float]]:
        result = []
        for possibleKeyWord in possibleKeyWords:
            keyword, data, *_ = possibleKeyWord.split('=')
            processingResult = self._extractRangeValuesFromString(data)
            if not processingResult:
                result.append([keyword, data])
            else:           
                val1, val2 = processingResult     
                buffer = [keyword] + [item for item in [val1, val2] if item]
                result.append(buffer)
        return result
    
    def _extractRangeValuesFromString(self, keywordData:str) -> None | tuple[float, float]:
        floatPattern = '(-?\d*(?:\.\d+)?)?' # checks for float 1.2, 0.2 .2 or int
        rangePattern = f'^\[{floatPattern};{floatPattern}]$' # checks if criteria is 2 numbers [1.2;2.3], 1 number [;1] or [1;] or [;]

        keywordData = keywordData.strip().replace(' ', '')        
        if re.search(rangePattern, keywordData):
            minVal, maxVal = keywordData[1:-1].split(';')
            minVal = float(minVal) if minVal else float('-inf')
            maxVal = float(maxVal) if maxVal else float('inf')
            return minVal, maxVal
        return None