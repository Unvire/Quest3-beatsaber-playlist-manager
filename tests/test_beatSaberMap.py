import pytest
import beatSaberMap
import datetime

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
    song.setNameAndHash('test song', 'BHVASJDVHasd')
    song.mapper = 'mapper'
    expected =  "Song: {'Name': 'test song', 'ID': '1234', 'Hash': 'BHVASJDVHasd', 'Mapper': 'mapper'}"
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

def test_getDataFromBeatSaverJSON(exampleJSON_data):
    song = beatSaberMap.BeatSaberMap('57c2')
    song.getDataFromBeatSaverJSON(exampleJSON_data)
    
    assert song.name == 'Rockefeller Street (Nightcore) -  Getter Jaani'
    assert song.id == '57c2'
    assert song.hash == 'b8c98ffc598703aadb4a3cb921d2830d270b57a5'

    assert song.title == 'Rockefeller Street (Nightcore)'
    assert song.author == 'Getter Jaani'
    assert song.mapper == 'RinkuSenpai'
    assert song.bpm == 162.5
    assert song.lengthSeconds == 145

    assert song.coverUrl == 'https://eu.cdn.beatsaver.com/b8c98ffc598703aadb4a3cb921d2830d270b57a5.jpg'
    assert song.previewUrl == 'https://eu.cdn.beatsaver.com/b8c98ffc598703aadb4a3cb921d2830d270b57a5.mp3'

    assert song.rankedState == 'Ranked'
    assert song.tagsList == ['pop']

    ## TEST LEVEL INSTANCES
    hardLevel = song.diffs[0]
    assert hardLevel.difficulty == 'Hard'
    assert hardLevel.characteristic == 'Standard'
    assert hardLevel.njs == 13
    assert hardLevel.nps == 3.884
    assert hardLevel.stars == 3.4
    assert hardLevel.requiredMods == ''

    expertLevel = song.diffs[1]
    assert expertLevel.difficulty == 'Expert'
    assert expertLevel.characteristic == 'Standard'
    assert expertLevel.njs == 17
    assert expertLevel.nps == 5.053
    assert expertLevel.stars == 3.7
    assert expertLevel.requiredMods == ''

def test_setRankedState():
    song = beatSaberMap.BeatSaberMap('57c2')

    song.setRankedState(isRanked=False, isQualified=False)
    assert song.rankedState == 'Graveyard'

    song.setRankedState(isRanked=False, isQualified=True)
    assert song.rankedState == 'Qualified'

    song.setRankedState(isRanked=True, isQualified=True)
    assert song.rankedState == 'Ranked'

    song.setRankedState(isRanked=True, isQualified=False)
    assert song.rankedState == 'Ranked'

def test_buildLongString(exampleJSON_data):
    song = beatSaberMap.BeatSaberMap('57c2')
    song.getDataFromBeatSaverJSON(exampleJSON_data)
    result = song.searchCache['longString']
    resultWords = sorted(result.split(' '))
    
    expected = ['(nightcore)', 'expert', 'getter', 'hard', 'jaani', 'pop', 'rinkusenpai', 'rockefeller', 'standard', 'street']
    assert resultWords == expected

def test_getRangesForEngineCache(exampleJSON_data):    
    song = beatSaberMap.BeatSaberMap('57c2')
    song.getDataFromBeatSaverJSON(exampleJSON_data)

    assert song.getStarsRange() == (3.4, 3.7)

    song.diffs[0].stars = '?' #assume that song is unranked and has '?' as stars value
    assert song.getStarsRange() == '?'
    assert song.getNpsRange() == (3.884, 5.053)
    assert song.getNjsRange() == (13, 17)
    assert song.getRequiredMods() == set()

    song.diffs[0].requiredMods = 'chroma, me'
    song.diffs[1].requiredMods = 'chroma, me'
    assert song.getRequiredMods() == set(['chroma', 'me'])

def test_getCacheData(exampleJSON_data):
    song = beatSaberMap.BeatSaberMap('57c2')
    song.getDataFromBeatSaverJSON(exampleJSON_data)
    result = song.getCacheData()

    resultWords = sorted(result['longString'].split(' '))
    expectedWords = ['(nightcore)', 'expert', 'getter', 'hard', 'jaani', 'pop', 'rinkusenpai', 'rockefeller', 'standard', 'street']
    assert resultWords == expectedWords

    assert result['length'] == 145
    assert result['bpm'] == 162.5
    assert result['mods'] == set()
    assert result['nps'] == (3.884, 5.053)
    assert result['njs'] == (13, 17)
    assert result['stars'] == (3.4, 3.7)
    assert result['rankedState'] == 'Ranked'