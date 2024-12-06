from beatSaberPlaylist import BeatSaberPlaylist
from beatSaberMap import BeatSaberMap

import re

class SearchEngine:
    def __init__(self):
        self.playlistHandle = None
        self.cache = {}

    def setPlaylistHandle(self, playlistInstance:BeatSaberPlaylist):
        for i, map in enumerate(playlistInstance):
            mapCache = self._cacheMapData(map)
            self.cache[i] = mapCache
    
    def _cacheMapData(self, mapInstance:BeatSaberMap):        
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