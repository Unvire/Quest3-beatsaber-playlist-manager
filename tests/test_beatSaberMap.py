import pytest
import beatSaberMap

def test_initAndRepr():
    song = beatSaberMap.BeatSaberMap('1234')
    song._setNameAndHash('test song', 'BHVASJDVHasd')
    song._setAuthorAndUrls('author', 'a', 'b')
    expected =  "Song: {'Name': 'test song', 'ID': '1234', 'Hash': 'BHVASJDVHasd', 'Author': 'author'}"
    assert song.__repr__() == expected

    