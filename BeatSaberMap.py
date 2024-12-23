import datetime, re
from beatSaberMapLevel import BeatSaberMapLevel

class BeatSaberMap:
    def __init__(self, id:str):        
        ## data for playlist entry
        self.id = id
        self.name = ''
        self.hash = ''

        ## metadata
        self.title = ''
        self.author = ''
        self.mapper = ''
        self.bpm = 0.0
        self.lengthSeconds = 0

        ## urls
        self.coverUrl = ''
        self.previewUrl = ''
        self.downloadUrl = ''

        self.rankedState = ''
        self.diffs = []
        self.tagsList = []
        self.uploaded = datetime.datetime.strptime('1970-01-01T00:00:00.000Z', '%Y-%m-%dT%H:%M:%S.%fZ')

        self.searchCache = {
            'longString': '',
            'length': '',
            'bpm': '',
            'mods': set(),
            'nps': '',
            'njs': '',
            'stars': '',
            'rankedState': set()
        }
    
    def __repr__(self) -> str:
        result = {
            'Name': self.name,
            'ID': self.id,
            'Hash': self.hash,
            'Mapper': self.mapper
            }
        return f'Song: {result}'
    
    def getDataFromBeatSaverJSON(self, responseJSON:dict):
        name = responseJSON['name']
        hash = responseJSON['versions'][0]['hash']
        self.setNameAndHash(name, hash)

        title = responseJSON['metadata']['songName']
        author = responseJSON['metadata']['songAuthorName']
        mapper = responseJSON['metadata']['levelAuthorName']
        bpm = responseJSON['metadata']['bpm']
        lengthSeconds = responseJSON['metadata']['duration']
        self.setMetadata(title, author, mapper, bpm, lengthSeconds)

        isRanked = responseJSON['ranked']
        isQualified = responseJSON['qualified']
        self.setRankedState(isRanked, isQualified)

        uploadedTimeStr = responseJSON['uploaded']
        uploadedDateTime = self.timeStrToDateTime(uploadedTimeStr)
        self.setUploaded(uploadedDateTime)
        
        try:
            tagsList = responseJSON['tags']        
            self.setTagsList(tagsList)
        except KeyError:
            pass
        
        coverUrl = responseJSON['versions'][0]['coverURL']
        previewUrl = responseJSON['versions'][0]['previewURL']
        downloadUrl = responseJSON['versions'][0]['downloadURL']
        self.setUrls(coverUrl, previewUrl, downloadUrl)
        
        levelsData = responseJSON['versions'][0]['diffs']
        diffsList = [BeatSaberMapLevel(diffData) for diffData in levelsData]
        self.setDiffs(diffsList)

        self._cacheData()
    
    def setNameAndHash(self, name:str, hash:str):
        self.name = name
        self.hash = hash
    
    def setMetadata(self, title:str, author:str, mapper:str, bpm:float, lengthSeconds:int):
        self.title = title
        self.author = author
        self.mapper = mapper
        self.bpm = float(bpm)
        self.lengthSeconds = int(lengthSeconds)
        
    def setRankedState(self, isRanked:bool, isQualified:bool):
        rankedDict = {
            '00': 'Graveyard',
            '01': 'Qualified',
            '10': 'Ranked',
            '11': 'Ranked'
        }
        key = f'{int(isRanked)}{int(isQualified)}'
        self.rankedState = rankedDict[key]
    
    def setTagsList(self, tagsList: list[str]):
        self.tagsList = tagsList
    
    def setUrls(self, coverUrl:str, previewUrl:str, downloadURL:str):
        self.coverUrl = coverUrl
        self.previewUrl = previewUrl
        self.downloadUrl = downloadURL
    
    def setDiffs(self, diffsList:list[BeatSaberMapLevel]):
        self.diffs = diffsList
    
    def getDiffs(self) -> list[BeatSaberMapLevel]:
        return self.diffs[:]
    
    def generateDictForPlaylist(self) -> dict:
        data = {
            'key': self.id,
            'hash': self.hash,
            'songName': self.name
        }
        return data

    def getCoverUrl(self) -> str:
        return self.coverUrl
    
    def getPreviewUrl(self) -> str:
        return self.previewUrl
    
    def timeStrToDateTime(self, timeStr:str) -> datetime.datetime:
        DATE_PATTERN = '^\d{4}-\d{2}-\d{2}.\d{2}:\d{2}:\d{2}Z$'
        timeStr = timeStr[:19] + 'Z'
        if re.search(DATE_PATTERN, timeStr):
            uploadedDateTime = datetime.datetime.strptime(timeStr, '%Y-%m-%dT%H:%M:%SZ')
        else:
            uploadedDateTime = datetime.datetime.strptime('1970-01-01T00:00:00.000Z', '%Y-%m-%dT%H:%M:%S.%fZ')
        return uploadedDateTime

    def setUploaded(self, uploadedDateTime:datetime.datetime):
        self.uploaded = uploadedDateTime

    def getCacheData(self) -> dict:
        return self.searchCache
    
    def _cacheData(self):
        self.searchCache['longString'] = self._buildLongString()
        self.searchCache['length'] = self.lengthSeconds
        self.searchCache['bpm'] = self.bpm
        self.searchCache['mods'] = self.getRequiredMods()
        self.searchCache['nps'] = self.getNpsRange()
        self.searchCache['njs'] = self.getNjsRange()
        self.searchCache['stars'] = self.getStarsRange()
        self.searchCache['rankedState'] = set([self.rankedState])
    
    def _buildLongString(self) -> str:
        words = set()
        words.add(self.title)
        words.add(self.author)
        words.add(self.mapper)

        for level in self.getDiffs():
            words.add(level.difficulty)
            words.add(level.characteristic)
        
        for tag in self.tagsList:
            words.add(tag)
        return ' '.join(list(words)).lower()
    
    def getStarsRange(self) -> str|tuple[float, float]:
        minVal, maxVal = self._getInitialMinMaxValues()
        for level in self.diffs:
            if level.stars == '?':
                return '?'
            minVal, maxVal = self._updateMinMaxValues(minVal, maxVal, level.stars)
        return self._tupleOrValue(minVal, maxVal)

    def getNpsRange(self) -> tuple[float, float]:
        minVal, maxVal = self._getInitialMinMaxValues()
        for level in self.diffs:
            minVal, maxVal = self._updateMinMaxValues(minVal, maxVal, level.nps)
        return self._tupleOrValue(minVal, maxVal)  
    
    def getNjsRange(self) -> tuple[float, float]:
        minVal, maxVal = self._getInitialMinMaxValues()
        for level in self.diffs:
            minVal, maxVal = self._updateMinMaxValues(minVal, maxVal, level.njs)
        return self._tupleOrValue(minVal, maxVal)
    
    def getRequiredMods(self) -> list[str]:
        mods = set()
        for level in self.diffs:
            modsString = level.requiredMods.replace(' ', '')
            for modName in modsString.split(','):
                if modName:
                    mods.add(modName)
        return mods

    def _tupleOrValue(self, val1:float, val2:float) -> tuple[float] | float:
        if val1 == val2:
            return val1
        return val1, val2

    def _updateMinMaxValues(self, currentMin:float, currentMax:float, val:float) -> tuple[float, float]:
        currentMin = min(currentMin, val)
        currentMax = max(currentMax, val)
        return currentMin, currentMax

    def _getInitialMinMaxValues(self) -> tuple[float, float]:
        minVal = float('inf')
        maxVal = float('-inf')
        return minVal, maxVal
    


if __name__ == '__main__':
    responseJSONMock = {
        "id": "57c2",
        "name": "Rockefeller Street (Nightcore) -  Getter Jaani",
        "description": "Hey this is reuploaded since it broke before\nhave fun",
        "uploader": {
            "id": 16388,
            "name": "rinkusenpai",
            "hash": "5cff0b7398cc5a672c84f6cc",
            "avatar": "https://www.gravatar.com/avatar/5cff0b7398cc5a672c84f6cc?d=retro",
            "type": "SIMPLE",
            "admin": False,
            "curator": False,
            "seniorCurator": False,
            "verifiedMapper": True,
            "playlistUrl": "https://api.beatsaver.com/users/id/16388/playlist"
        },
        "metadata": {
            "bpm": 162.5,
            "duration": 145,
            "songName": "Rockefeller Street (Nightcore)",
            "songSubName": "",
            "songAuthorName": "Getter Jaani",
            "levelAuthorName": "RinkuSenpai"
        },
        "stats": {
            "plays": 0,
            "downloads": 0,
            "upvotes": 13013,
            "downvotes": 575,
            "score": 0.9559,
            "reviews": 8,
            "sentiment": "VERY_POSITIVE"
        },
        "uploaded": "2019-07-18T21:40:09.204Z",
        "automapper": False,
        "ranked": True,
        "qualified": False,
        "versions": [
            {
                "hash": "b8c98ffc598703aadb4a3cb921d2830d270b57a5",
                "key": "57c2",
                "state": "Published",
                "createdAt": "2019-07-18T21:40:09.204Z",
                "sageScore": 6,
                "diffs": [
                    {
                        "njs": 13,
                        "offset": 0,
                        "notes": 545,
                        "bombs": 0,
                        "obstacles": 8,
                        "nps": 3.884,
                        "length": 380,
                        "characteristic": "Standard",
                        "difficulty": "Hard",
                        "events": 2247,
                        "chroma": False,
                        "me": False,
                        "ne": False,
                        "cinema": False,
                        "seconds": 140.308,
                        "paritySummary": {
                            "errors": 73,
                            "warns": 61,
                            "resets": 0
                        },
                        "stars": 3.4,
                        "maxScore": 494155,
                        "environment": "NiceEnvironment"
                    },
                    {
                        "njs": 17,
                        "offset": 0,
                        "notes": 709,
                        "bombs": 0,
                        "obstacles": 6,
                        "nps": 5.053,
                        "length": 380,
                        "characteristic": "Standard",
                        "difficulty": "Expert",
                        "events": 2247,
                        "chroma": False,
                        "me": False,
                        "ne": False,
                        "cinema": False,
                        "seconds": 140.308,
                        "paritySummary": {
                            "errors": 87,
                            "warns": 75,
                            "resets": 0
                        },
                        "stars": 3.7,
                        "maxScore": 645035,
                        "environment": "NiceEnvironment"
                    }
                ],
                "downloadURL": "https://r2cdn.beatsaver.com/b8c98ffc598703aadb4a3cb921d2830d270b57a5.zip",
                "coverURL": "https://eu.cdn.beatsaver.com/b8c98ffc598703aadb4a3cb921d2830d270b57a5.jpg",
                "previewURL": "https://eu.cdn.beatsaver.com/b8c98ffc598703aadb4a3cb921d2830d270b57a5.mp3"
            }
        ],
        "createdAt": "2019-07-18T21:40:09.204Z",
        "updatedAt": "2019-07-18T21:40:09.204Z",
        "lastPublishedAt": "2019-07-18T21:40:09.204Z",
        "tags": [
            "pop"
        ],
        "bookmarked": False,
        "declaredAi": "None",
        "blRanked": False,
        "blQualified": False
    }
    

    beatmap = BeatSaberMap('57c2')
    beatmap.getDataFromBeatSaverJSON(responseJSONMock)
    print(beatmap)