import requests

class BeatSaberMap:
    def __init__(self, id:str):
        self.name = ''
        self.id = id
        self.hash = ''
        self.beatsaverMapInfoAPI = 'https://api.beatsaver.com/maps/id/'
    
    def __repr__(self) -> str:
        result = {
            'Name': self.name,
            'ID': self.id,
            'Hash': self.hash
            }
        return f'Song: {result}'
    
    def getDataFromBeatSaverApi(self):
        url = self.beatsaverMapInfoAPI + self.id
        responseJSON = requests.get(url).json()

        name = responseJSON['name']
        hash = responseJSON['versions'][0]['hash']
        self._setNameAndHash(name, hash)
    
    def _setNameAndHash(self, name:str, hash:str):
        self.name = name
        self.hash = hash


if __name__ == '__main__':
    beatmap = BeatSaberMap('57c2')
    beatmap.getDataFromBeatSaverApi()
    print(beatmap)