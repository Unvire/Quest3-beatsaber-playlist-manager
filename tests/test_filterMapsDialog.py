import pytest, os, json
from filterMapsDialog import FilterMapsDialog
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

@pytest.mark.parametrize('inputData, expected', [
    ('ksdmladm', 'ksdmladm'), ('', ''), ('Ranked', 'Ranked'), ('[1]', '[1]'),  ('[1.1213123123123;]', (1.1213123123123, float('inf'))), 
    ('3;3', '3;3'), ('[3; 3.5]', (3, 3.5)), ('[;]', (float('-inf'), float('inf'))), ('[;2]', (float('-inf'), 2)), ('[2; -2]', (2, -2)), (';', ';')
                                                ])
def test__extractRangeValuesFromString(inputData, expected):
    assert FilterMapsDialog._extractRangeValuesFromString(None, inputData) == expected

@pytest.mark.parametrize('inputCacheValue, inputRequiredValue, expected', [
    ((1, 3), (0, 3), False), ((1, 3), (2, 3), True), ((0, 4), (2, 3), True), ((2, 3), (2, 3), True), ((2, 3), (3, 2), True), ((2, 3), (0, 4), False), ((0, 2), (0, 3), False),
    (2, (0, 3), True), (-2, (0, 3), False), (0, (0, 3), True), (3, (0, 3), True),
    ('test', 'test', True), ('test', '', False)])
def test__checkRangeOrStr(inputCacheValue, inputRequiredValue, expected):
    assert FilterMapsDialog._checkRangeOrStr(None, inputCacheValue, inputRequiredValue) == expected

def test__filterMaps(mockPlaylist):
  
    
    FilterMapsDialog._filterMaps(None, mockPlaylist)