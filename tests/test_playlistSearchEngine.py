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

def test__findLongStringsAndKeywords():
    request = 'test __test __test__ __test= !(@#*),asndm, __length=1230210, __bpm=uavds'
    instance = playlistSearchEngine.SearchEngine()
    longStrings, keywords = instance._findKeywords(request)

    assert longStrings == ['test', '__test', '__test__', '__test=', '!(@#*),asndm,']
    assert keywords == ['__length=1230210,', '__bpm=uavds']

@pytest.mark.parametrize("inputData, expected", [
    ('ksdmladm', None), ('', None), ('Ranked', None), ('[1]', None),  ('[1.1213123123123;]', (1.1213123123123, float('inf'))), 
    ('3;3', None), ('[3; 3.5]', (3, 3.5)), ('[;]', (float('-inf'), float('inf'))), ('[;2]', (float('-inf'), 2)), ('[2; -2]', (2, -2)), (';', None)
                                                ])
def test__extractRangeValuesFromString(inputData, expected):
    instance = playlistSearchEngine.SearchEngine()
    assert instance._extractRangeValuesFromString(inputData) == expected