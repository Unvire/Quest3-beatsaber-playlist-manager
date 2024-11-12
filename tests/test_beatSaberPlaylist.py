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

    

