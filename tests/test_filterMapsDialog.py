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

@pytest.mark.parametrize("inputData, expected", [
    ('ksdmladm', 'ksdmladm'), ('', ''), ('Ranked', 'Ranked'), ('[1]', '[1]'),  ('[1.1213123123123;]', (1.1213123123123, float('inf'))), 
    ('3;3', '3;3'), ('[3; 3.5]', (3, 3.5)), ('[;]', (float('-inf'), float('inf'))), ('[;2]', (float('-inf'), 2)), ('[2; -2]', (2, -2)), (';', ';')
                                                ])
def test__extractRangeValuesFromString(inputData, expected):
    assert FilterMapsDialog._extractRangeValuesFromString(None, inputData) == expected