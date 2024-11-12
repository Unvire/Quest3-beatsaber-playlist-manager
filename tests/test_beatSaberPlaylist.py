import pytest
import beatSaberPlaylist

@pytest.mark.parametrize("inputData, expected", [([2, 7, 5, 4], [[2], [4, 5], [7]]), 
                                                 ([1], [[1]]), ([1, 2], [[1, 2]]), ([], [[]]),
                                                 ([1, 2, 3, 4, 10, 11, 12, 13], [[1, 2, 3, 4], [10, 11, 12, 13]]),
                                                 ([1, 3, 5, 7, 9], [[1], [3], [5], [7], [9]])
                                                ])
def test__makeSelectionGroups(inputData, expected):
    instance = beatSaberPlaylist.BeatSaberPlaylist()
    instance._selectedIndexes = set(inputData)
    assert expected == instance._makeSelectionGroups()
    