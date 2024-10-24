import requests

class BeatSaberMap:
    def __init__(self, id:str):
        self.name = ''
        self.id = id
        self.hash = ''
        self.beatsaverMapInfoAPI = 'https://api.beatsaver.com/maps/id/'
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
        url = self.beatsaverMapInfoAPI + self.id
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


if __name__ == '__main__':
    beatmap = BeatSaberMap('57c2')
    beatmap.getDataFromBeatSaverApi()
    print(beatmap)