import requests

class BeatSaberMap:
    BEATSAVER_API_URL = 'https://api.beatsaver.com/maps/id/'
    def __init__(self, id:str):
        self.name = ''
        self.id = id
        self.hash = ''
        self.author = ''
        self.coverUrl = ''
        self.previewUrl = ''
        self.diffs = []
    
    def __repr__(self) -> str:
        result = {
            'Name': self.name,
            'ID': self.id,
            'Hash': self.hash,
            'Author': self.author
            }
        return f'Song: {result}'
    
    def getDataFromBeatSaverApi(self):
        url = BeatSaberMap.BEATSAVER_API_URL + self.id
        responseJSON = requests.get(url).json()

        name = responseJSON['name']
        hash = responseJSON['versions'][0]['hash']
        self._setNameAndHash(name, hash)

        author = responseJSON['uploader']['name']
        coverUrl = responseJSON['versions'][0]['coverURL']
        previewUrl = responseJSON['versions'][0]['previewURL']
        self._setAuthorAndUrls(author, coverUrl, previewUrl)
        
        levelsData = responseJSON['versions'][0]['diffs']
        diffsList = [diffData['difficulty'] for diffData in levelsData]
        self._setDiffs(diffsList)
    
    def _setNameAndHash(self, name:str, hash:str):
        self.name = name
        self.hash = hash
    
    def _setAuthorAndUrls(self, author:str, coverUrl:str, previewUrl):
        self.author = author
        self.coverUrl = coverUrl
        self.previewUrl = previewUrl
    
    def _setDiffs(self, diffsList:list[str]):
        self.diffs = diffsList
    
    def getDiffs(self) -> list[str]:
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

if __name__ == '__main__':
    beatmap = BeatSaberMap('57c2')
    beatmap.getDataFromBeatSaverApi()
    print(beatmap)