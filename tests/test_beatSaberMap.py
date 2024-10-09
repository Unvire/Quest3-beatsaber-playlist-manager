import pytest
import beatSaberMap

def test_initAndRepr():
    song = beatSaberMap.BeatSaberMap('1234')
    song._setNameAndHash('test song', 'BHVASJDVHasd')
    expected =  "Song: {'Name': 'test song', 'ID': '1234', 'Hash': 'BHVASJDVHasd'}"
    assert song.__repr__() == expected