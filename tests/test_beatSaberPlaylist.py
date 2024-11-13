import pytest
import beatSaberPlaylist

def test_select():
    instance = beatSaberPlaylist.BeatSaberPlaylist()
    instance.songsList = [i for i in range(20)]

    instance.select(-1)
    assert instance._selectedIndexes == []
    instance.select(0)
    assert instance._selectedIndexes == [0]
    instance.select(10)
    assert instance._selectedIndexes == [0, 10]
    instance.select(0)
    assert instance._selectedIndexes == [0, 10]
    instance.select(1)
    assert instance._selectedIndexes == [0, 1, 10]
    instance.select(9)
    assert instance._selectedIndexes == [0, 1, 9, 10]
    instance.select(11)
    assert instance._selectedIndexes == [0, 1, 9, 10, 11]

def test__unselectedIndexes():
    instance = beatSaberPlaylist.BeatSaberPlaylist()
    instance.songsList = [i for i in range(10)]
    instance._selectedIndexes = [2, 4, 5, 7]
    assert instance._getUnselectedIndexes() == [0, 1, 3, 6, 8, 9]

@pytest.mark.parametrize("inputData, expected", [([2, 7, 5, 4], [[2], [4, 5], [7]]), 
                                                 ([1], [[1]]), 
                                                 ([1, 2], [[1, 2]]), 
                                                 ([], [[]]),
                                                 ([1, 2, 3, 4, 10, 11, 12, 13], [[1, 2, 3, 4], [10, 11, 12, 13]]),
                                                 ([1, 3, 5, 7, 9], [[1], [3], [5], [7], [9]])
                                                ])
def test__makeSelectionGroups(inputData, expected):
    instance = beatSaberPlaylist.BeatSaberPlaylist()
    assert expected == instance._makeSelectionGroups(inputData)

@pytest.mark.parametrize("inputData, expected", [
                                                 ([2, 4, 5, 7], [0, 2, 1, 4, 5, 3, 7, 6, 8, 9]),
                                                 ([0, 1], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
                                                 ([7, 8, 9], [0, 1, 2, 3, 4, 5, 7, 8, 9, 6]),
                                                 ([1], [1, 0, 2, 3, 4, 5, 6, 7, 8, 9]),
                                                 ([8], [0, 1, 2, 3, 4, 5, 6, 8, 7, 9]),
                                                 ([2, 3, 4, 5], [0, 2, 3, 4, 5, 1, 6, 7, 8, 9]),                                                 
                                                 ([0, 1, 9], [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]),
                                                 ([1, 3, 5, 7, 9], [1, 0, 3, 2, 5, 4, 7, 6, 9, 8]),
                                                 ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
                                                ])
def test__calculateIndexesAfterMoveUp(inputData, expected):
    instance = beatSaberPlaylist.BeatSaberPlaylist()
    instance.songsList = [i for i in range(10)]

    instance._selectedIndexes = inputData
    assert instance._calculateIndexesAfterMoveUp() == expected

@pytest.mark.parametrize("inputData, expected", [
                                                 ([2, 4, 5, 7], [0, 1, 3, 2, 6, 4, 5, 8, 7, 9]),
                                                 ([0, 1], [2, 0, 1, 3, 4, 5, 6, 7, 8, 9]),                                                 
                                                 ([7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
                                                 ([1], [0, 2, 1, 3, 4, 5, 6, 7, 8, 9]),                                                 
                                                 ([8], [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]),
                                                 ([2, 3, 4, 5], [0, 1, 6, 2, 3, 4, 5, 7, 8, 9]),
                                                 ([0, 1, 9], [2, 0, 1, 3, 4, 5, 6, 7, 8, 9]),
                                                 ([0, 2, 4, 6, 8], [1, 0, 3, 2, 5, 4, 7, 6, 9, 8]),
                                                 ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
                                                ])
def test__calculateIndexesAfterMoveDown(inputData, expected):
    instance = beatSaberPlaylist.BeatSaberPlaylist()
    instance.songsList = [i for i in range(10)]

    instance._selectedIndexes = inputData
    assert instance._calculateIndexesAfterMoveDown() == expected

@pytest.mark.parametrize("inputData, expected", [([2, 7, 5, 4], [1, 3, 4, 6]), 
                                                 ([1], [0]), 
                                                 ([1, 2], [0, 1]), 
                                                 ([], []),
                                                 ([0, 1], [0, 1]),
                                                 ([0, 1, 7, 8, 11, 12], [0, 1, 6, 7, 10, 11]),
                                                 ([0, 1, 3, 4], [0, 1, 2, 3])
                                                ])
def test__updateSelectedIndexesAfterMoveUp(inputData, expected):
    instance = beatSaberPlaylist.BeatSaberPlaylist()
    instance._selectedIndexes = inputData
    assert instance._updateSelectedIndexesAfterMoveUp() == expected

@pytest.mark.parametrize("inputData, expected", [ #0a, 1b, 2c 3d 4e 5f 6g 7h 8i 9j
                                                 ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']),
                                                 ([0, 1, 3, 2, 6, 4, 5, 8, 7, 9], ['a', 'b', 'd', 'c', 'g', 'e', 'f', 'i', 'h', 'j']),
                                                 ([2, 0, 1, 3, 4, 5, 6, 7, 8, 9], ['c', 'a', 'b', 'd', 'e', 'f', 'g', 'h', 'i', 'j']), 
                                                 ([0, 2, 1, 3, 4, 5, 6, 7, 8, 9], ['a', 'c', 'b', 'd', 'e', 'f', 'g', 'h', 'i', 'j']),
                                                 ([0, 1, 6, 2, 3, 4, 5, 7, 8, 9], ['a', 'b', 'g', 'c', 'd', 'e', 'f', 'h', 'i', 'j']),
                                                 ([1, 0, 3, 2, 5, 4, 7, 6, 9, 8], ['b', 'a', 'd', 'c', 'f', 'e', 'h', 'g', 'j', 'i']),
                                                ])
def test__reorderSongs(inputData, expected):
    instance = beatSaberPlaylist.BeatSaberPlaylist()
    instance.songsList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    assert instance._reorderSongs(inputData) == expected