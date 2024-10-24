import pytest
import beatSaberMap

def test_initAndRepr():
    song = beatSaberMap.BeatSaberMap('1234')
    song._setNameAndHash('test song', 'BHVASJDVHasd')
    song._setAuthorAndUrls('author', 'a', 'b')
    expected =  "Song: {'Name': 'test song', 'ID': '1234', 'Hash': 'BHVASJDVHasd', 'Author': 'author'}"
    assert song.__repr__() == expected

def test_generateDictForPlaylist():
    song = beatSaberMap.BeatSaberMap('1234')
    song.hash = 'eae95f9d7700b2e9b724ffe5ad23b4541f701181'
    song.name = 'test song'
    expected = {
        'key': '1234',
        'hash': 'eae95f9d7700b2e9b724ffe5ad23b4541f701181',
        'songName': 'test song'
    }
    assert song.generateDictForPlaylist() == expected