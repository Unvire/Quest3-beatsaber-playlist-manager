import pytest
import beatSaberMap

@pytest.fixture
def exampleJSON_data():
    response = {
        "id": "57c2",
        "name": "Rockefeller Street (Nightcore) -  Getter Jaani",
        "description": "Hey this is reuploaded since it broke before\nhave fun",
        "uploader": {
            "id": 16388,
            "name": "rinkusenpai",
            "hash": "5cff0b7398cc5a672c84f6cc",
            "avatar": "https://www.gravatar.com/avatar/5cff0b7398cc5a672c84f6cc?d=retro",
            "type": "SIMPLE",
            "admin": False,
            "curator": False,
            "seniorCurator": False,
            "verifiedMapper": True,
            "playlistUrl": "https://api.beatsaver.com/users/id/16388/playlist"
        },
        "metadata": {
            "bpm": 162.5,
            "duration": 145,
            "songName": "Rockefeller Street (Nightcore)",
            "songSubName": "",
            "songAuthorName": "Getter Jaani",
            "levelAuthorName": "RinkuSenpai"
        },
        "stats": {
            "plays": 0,
            "downloads": 0,
            "upvotes": 13005,
            "downvotes": 575,
            "score": 0.9559,
            "reviews": 8,
            "sentiment": "VERY_POSITIVE"
        },
        "uploaded": "2019-07-18T21:40:09.204Z",
        "automapper": False,
        "ranked": True,
        "qualified": False,
        "versions": [
            {
                "hash": "b8c98ffc598703aadb4a3cb921d2830d270b57a5",
                "key": "57c2",
                "state": "Published",
                "createdAt": "2019-07-18T21:40:09.204Z",
                "sageScore": 6,
                "diffs": [
                    {
                        "njs": 13,
                        "offset": 0,
                        "notes": 545,
                        "bombs": 0,
                        "obstacles": 8,
                        "nps": 3.884,
                        "length": 380,
                        "characteristic": "Standard",
                        "difficulty": "Hard",
                        "events": 2247,
                        "chroma": False,
                        "me": False,
                        "ne": False,
                        "cinema": False,
                        "seconds": 140.308,
                        "paritySummary": {
                            "errors": 73,
                            "warns": 61,
                            "resets": 0
                        },
                        "stars": 3.4,
                        "maxScore": 494155
                    },
                    {
                        "njs": 17,
                        "offset": 0,
                        "notes": 709,
                        "bombs": 0,
                        "obstacles": 6,
                        "nps": 5.053,
                        "length": 380,
                        "characteristic": "Standard",
                        "difficulty": "Expert",
                        "events": 2247,
                        "chroma": False,
                        "me": False,
                        "ne": False,
                        "cinema": False,
                        "seconds": 140.308,
                        "paritySummary": {
                            "errors": 87,
                            "warns": 75,
                            "resets": 0
                        },
                        "stars": 3.7,
                        "maxScore": 645035
                    }
                ],
                "downloadURL": "https://r2cdn.beatsaver.com/b8c98ffc598703aadb4a3cb921d2830d270b57a5.zip",
                "coverURL": "https://eu.cdn.beatsaver.com/b8c98ffc598703aadb4a3cb921d2830d270b57a5.jpg",
                "previewURL": "https://eu.cdn.beatsaver.com/b8c98ffc598703aadb4a3cb921d2830d270b57a5.mp3"
            }
        ],
        "createdAt": "2019-07-18T21:40:09.204Z",
        "updatedAt": "2019-07-18T21:40:09.204Z",
        "lastPublishedAt": "2019-07-18T21:40:09.204Z",
        "tags": [
            "pop"
        ],
        "bookmarked": False,
        "declaredAi": "None",
        "blRanked": False,
        "blQualified": False
    }
    return response

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

def test_getDataFromBeatSaverApi(exampleJSON_data):
    song = beatSaberMap.BeatSaberMap('57c2')
    song.getDataFromJSON(exampleJSON_data)
    
    assert song.name == 'Rockefeller Street (Nightcore) -  Getter Jaani'
    assert song.id == '57c2'
    assert song.hash == 'b8c98ffc598703aadb4a3cb921d2830d270b57a5'
    assert song.author == 'rinkusenpai'
    assert song.coverUrl == 'https://eu.cdn.beatsaver.com/b8c98ffc598703aadb4a3cb921d2830d270b57a5.jpg'
    assert song.previewUrl == 'https://eu.cdn.beatsaver.com/b8c98ffc598703aadb4a3cb921d2830d270b57a5.mp3'
    assert song.diffs == ['Hard', 'Expert']

