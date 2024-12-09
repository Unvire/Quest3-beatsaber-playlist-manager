import pytest, os, json
import playlistSearchEngine
import beatSaberMap, beatSaberMapLevel, beatSaberPlaylist

@pytest.fixture
def mockPlaylist():
    jsonMockDumpPath = os.path.join(os.getcwd(), 'testFiles', '10songsJSON.txt')    
    with open(jsonMockDumpPath) as file:
        fileLines = ''.join(file.readlines())
        mockJsonResponse = json.loads(fileLines)

    playlist = beatSaberPlaylist.BeatSaberPlaylist()
    for key, mapJSON in mockJsonResponse.items():
            playlist._addMapFromJSON(key, mapJSON)
    return playlist

def test_buildLongString(mockPlaylist):
    instance = playlistSearchEngine.SearchEngine()
    result = instance._buildLongString(mockPlaylist[1])
    resultWords = sorted(result.split(' '))

    expectedWords = ['Expert', 'ExpertPlus', 'Hard', 'HickeyChan', 'Inabakumori', 'Lagtrain', 'Lawless', 'challenge', 'pop', 'tech', 'vocaloid']
    assert resultWords == expectedWords
    