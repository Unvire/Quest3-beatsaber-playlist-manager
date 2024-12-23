import pytest, os, json
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from filterMapsDialog import FilterMapsDialog
import beatSaberMap, beatSaberMapLevel, beatSaberPlaylist

@pytest.fixture
def mockPlaylist():
    path = os.path.dirname(__file__)
    jsonMockDumpPath = os.path.join(path, 'testFiles', '8songsJSON.txt')    
    with open(jsonMockDumpPath) as file:
        fileLines = ''.join(file.readlines())
        mockJsonResponse = json.loads(fileLines)

    playlist = beatSaberPlaylist.BeatSaberPlaylist()
    for key, mapJSON in mockJsonResponse.items():
            playlist._addMapFromJSON(key, mapJSON)
    return playlist

@pytest.fixture
def mockApp(qtbot, mockPlaylist):
    path = os.path.dirname(__file__)
    pathParts = path.split('\\')[:-1]
    newPath = '\\'.join(pathParts)
    os.chdir(newPath)
    window = FilterMapsDialog(mockPlaylist)
    qtbot.addWidget(window)
    return window

def test_windowInit(mockApp):
    mockApp

@pytest.mark.parametrize('inputData, expected', [
    ('ksdmladm', 'ksdmladm'), ('', ''), ('Ranked', 'Ranked'), ('[1]', '[1]'),  ('[1.1213123123123;]', (1.1213123123123, float('inf'))), 
    ('3;3', '3;3'), ('[3; 3.5]', (3, 3.5)), ('[;]', (float('-inf'), float('inf'))), ('[;2]', (float('-inf'), 2)), ('[2; -2]', (2, -2)), (';', ';')
                                                ])
def test__extractRangeValuesFromString(inputData, expected, mockApp):
    assert mockApp._extractRangeValuesFromString(inputData) == expected

def test__filterMaps_noCritertia(mockApp):    
    assert mockApp._filterMaps() == []

def test__filterMaps_longString(mockApp):
    assert mockApp._filterMaps(longStringPattern='expert') == [0]
    assert mockApp._filterMaps(longStringPattern='hard') == [4, 6]
    assert mockApp._filterMaps(longStringPattern='hard ') == [4, 6, 7]
    assert mockApp._filterMaps(longStringPattern='(hard|pop)') == [4, 6]

    assert mockApp._filterMaps(requiredLength=(100, 200)) == [0, 1, 3, 4, 7]
    assert mockApp._filterMaps(longStringPattern='expert', requiredLength=(100, 200)) == [0, 1, 3, 4, 7]

    assert mockApp._filterMaps(requiredBpm=184, requiredLength=(100, 200)) == [0, 1, 2, 3, 4, 5, 7]
    assert mockApp._filterMaps(requiredBpm=184, requiredLength=(100, 200), requiredNps=4) == [0, 1, 2, 3, 4, 5, 6, 7]