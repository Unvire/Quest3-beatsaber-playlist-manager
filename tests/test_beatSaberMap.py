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

def test_getDataFromBeatSaverApi():
    song = beatSaberMap.BeatSaberMap('57c2')
    song.getDataFromBeatSaverApi()
    
    assert song.name == 'Rockefeller Street (Nightcore) -  Getter Jaani'
    assert song.id == '57c2'
    assert song.hash == 'b8c98ffc598703aadb4a3cb921d2830d270b57a5'
    assert song.author == 'rinkusenpai'
    assert song.coverUrl == 'https://eu.cdn.beatsaver.com/b8c98ffc598703aadb4a3cb921d2830d270b57a5.jpg'
    assert song.previewUrl == 'https://eu.cdn.beatsaver.com/b8c98ffc598703aadb4a3cb921d2830d270b57a5.mp3'
    assert song.diffs == ['Hard', 'Expert']

