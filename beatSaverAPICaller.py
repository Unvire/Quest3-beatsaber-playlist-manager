import requests

class NotBeatSaverMap(Exception):
    pass

class BeatSaverAPICaller:
    SIGNLE_MAP_CALL_LINK = 'https://api.beatsaver.com/maps/id/'
    MULTIPLE_MAP_CALL_LINK = 'https://api.beatsaver.com/maps/ids/'
    MULTIPLE_MAP_CALL_LIST_LENGTH = 40

    @staticmethod
    def singleMapCall(mapID:str) -> dict:
        url = BeatSaverAPICaller.SIGNLE_MAP_CALL_LINK + mapID
        responseJSON = requests.get(url).json()
        
        if 'success' in responseJSON:
            raise NotBeatSaverMap
        
        return responseJSON

    @staticmethod
    def multipleMapsCall(mapIDList:list[str]) -> dict:
        COMMA_SEPARATOR = '%2C'

        subLists = BeatSaverAPICaller.splitListToChunks(mapIDList)
        result = {}
        for subList in subLists:
            idsString = COMMA_SEPARATOR.join(subList)
            url = BeatSaverAPICaller.MULTIPLE_MAP_CALL_LINK + idsString
            print(url)
            responseJSON = requests.get(url).json()
            result.update(responseJSON)
        return result
    
    def splitListToChunks(items:list) -> list[list]:        
        chunkSize = BeatSaverAPICaller.MULTIPLE_MAP_CALL_LIST_LENGTH
        fullChunks, lastChunk = divmod(len(items), chunkSize)
        
        result = []
        for i in range(fullChunks):
            iStart = chunkSize * i
            iEnd = chunkSize * (i + 1)
            result.append(items[iStart:iEnd])

        if lastChunk:
            iStart =  chunkSize * (i + 1) if fullChunks else 0
            result.append(items[iStart:])
        return result

if __name__ == '__main__':
    import os

    response = BeatSaverAPICaller.singleMapCall('57c2')

    mapsIDsPath = os.path.join(os.getcwd(), 'other', 'ls_questSongs.txt')
    with open(mapsIDsPath, 'r', encoding='utf-8') as file:
        buffer = file.readlines()

    songsIDsList = [line.split('\\')[0] for line in buffer]
    response = BeatSaverAPICaller.multipleMapsCall(songsIDsList)