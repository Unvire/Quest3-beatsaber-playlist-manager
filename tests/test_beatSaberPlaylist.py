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


@pytest.mark.parametrize("inputData, expected", [
                                                 ([2, 4, 5, 7], [0, 2, 1, 4, 5, 3, 7, 6, 8, 9]),
                                                 ([0, 1], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
                                                 ([1], [1, 0, 2, 3, 4, 5, 6, 7, 8, 9]),
                                                 ([2, 3, 4, 5], [0, 2, 3, 4, 5, 1, 6, 7, 8, 9]),
                                                 ([7, 8, 9], [0, 1, 2, 3, 4, 5, 7, 8, 9, 6]),
                                                 ([0, 1, 9], [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]),
                                                 ([1, 3, 5, 7, 9], [1, 0, 3, 2, 5, 4, 7, 6, 9, 8]),
                                                 ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
                                                ])
def test__calculateIndexesAfterMoveUp(inputData, expected):
    instance = beatSaberPlaylist.BeatSaberPlaylist()
    instance.songsList = [i for i in range(10)]

    instance._selectedIndexes = inputData
    print(inputData)
    print(instance._calculateIndexesAfterMoveUp())
    assert instance._calculateIndexesAfterMoveUp() == expected


@pytest.mark.parametrize("inputData, expected", [([2, 7, 5, 4], [[2], [4, 5], [7]]), 
                                                 ([1], [[1]]), ([1, 2], [[1, 2]]), ([], [[]]),
                                                 ([1, 2, 3, 4, 10, 11, 12, 13], [[1, 2, 3, 4], [10, 11, 12, 13]]),
                                                 ([1, 3, 5, 7, 9], [[1], [3], [5], [7], [9]])
                                                ])
def test__makeSelectionGroups(inputData, expected):
    instance = beatSaberPlaylist.BeatSaberPlaylist()
    assert expected == instance._makeSelectionGroups(inputData)
    
