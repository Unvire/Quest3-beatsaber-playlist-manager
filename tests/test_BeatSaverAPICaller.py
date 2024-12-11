import pytest
import beatSaverAPICaller

@pytest.fixture
def multipleCallExpected():
    response = {
    "57c2": {
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
                        "maxScore": 494155,
                        "environment": "NiceEnvironment"
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
                        "maxScore": 645035,
                        "environment": "NiceEnvironment"
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
    },
    "12b62": {
        "id": "12b62",
        "name": "USAO - Climax [Ranked]",
        "description": "Thanks to Kival and Scoop for modding\n\nThanks to Shrado for good audio quality, again.\n",
        "uploader": {
            "id": 4285482,
            "name": "Timbo",
            "hash": "5f187e6527b8b1000788ef07",
            "avatar": "https://cdn.beatsaver.com/avatar/64bc122e1b62e32794795e8806451534ecab7775.png",
            "type": "DISCORD",
            "admin": False,
            "curator": False,
            "seniorCurator": False,
            "verifiedMapper": True,
            "playlistUrl": "https://api.beatsaver.com/users/id/4285482/playlist"
        },
        "metadata": {
            "bpm": 190,
            "duration": 155,
            "songName": "Climax",
            "songSubName": "",
            "songAuthorName": "USAO",
            "levelAuthorName": "Timbo"
        },
        "uploaded": "2021-01-14T11:56:39.803Z",
        "automapper": False,
        "ranked": True,
        "qualified": False,
        "versions": [
            {
                "hash": "fd34b0279836820254c31552c5753291acbcbb95",
                "key": "12b62",
                "state": "Published",
                "createdAt": "2021-01-14T11:56:39.803Z",
                "sageScore": 7,
                "diffs": [
                    {
                        "njs": 14,
                        "offset": -0.75,
                        "notes": 549,
                        "bombs": 0,
                        "obstacles": 199,
                        "nps": 3.622,
                        "length": 480,
                        "characteristic": "Standard",
                        "difficulty": "Easy",
                        "events": 7552,
                        "chroma": False,
                        "me": False,
                        "ne": False,
                        "cinema": False,
                        "seconds": 151.579,
                        "paritySummary": {
                            "errors": 0,
                            "warns": 0,
                            "resets": 0
                        },
                        "stars": 2.64,
                        "maxScore": 497835,
                        "label": "RELAX",
                        "blStars": 3.47,
                        "environment": "DefaultEnvironment"
                    },
                    {
                        "njs": 16,
                        "offset": 0.5,
                        "notes": 814,
                        "bombs": 0,
                        "obstacles": 191,
                        "nps": 5.37,
                        "length": 480,
                        "characteristic": "Standard",
                        "difficulty": "Normal",
                        "events": 7552,
                        "chroma": False,
                        "me": False,
                        "ne": False,
                        "cinema": False,
                        "seconds": 151.579,
                        "paritySummary": {
                            "errors": 0,
                            "warns": 0,
                            "resets": 0
                        },
                        "stars": 3.44,
                        "maxScore": 741635,
                        "label": "REFLEX",
                        "blStars": 5.18,
                        "environment": "DefaultEnvironment"
                    },
                    {
                        "njs": 18,
                        "offset": 0.2,
                        "notes": 1019,
                        "bombs": 0,
                        "obstacles": 148,
                        "nps": 6.723,
                        "length": 480,
                        "characteristic": "Standard",
                        "difficulty": "Hard",
                        "events": 7552,
                        "chroma": False,
                        "me": False,
                        "ne": False,
                        "cinema": False,
                        "seconds": 151.579,
                        "paritySummary": {
                            "errors": 0,
                            "warns": 0,
                            "resets": 0
                        },
                        "stars": 5.19,
                        "maxScore": 930235,
                        "label": "COMPLEX",
                        "blStars": 6.34,
                        "environment": "DefaultEnvironment"
                    },
                    {
                        "njs": 19,
                        "offset": 0,
                        "notes": 1489,
                        "bombs": 4,
                        "obstacles": 113,
                        "nps": 9.823,
                        "length": 480,
                        "characteristic": "Standard",
                        "difficulty": "Expert",
                        "events": 7552,
                        "chroma": False,
                        "me": False,
                        "ne": False,
                        "cinema": False,
                        "seconds": 151.579,
                        "paritySummary": {
                            "errors": 0,
                            "warns": 0,
                            "resets": 1
                        },
                        "stars": 7.48,
                        "maxScore": 1362635,
                        "label": "CLIMAX",
                        "blStars": 8.12,
                        "environment": "DefaultEnvironment"
                    },
                    {
                        "njs": 21,
                        "offset": -0.3,
                        "notes": 1603,
                        "bombs": 4,
                        "obstacles": 111,
                        "nps": 10.575,
                        "length": 480.031,
                        "characteristic": "Standard",
                        "difficulty": "ExpertPlus",
                        "events": 7808,
                        "chroma": False,
                        "me": False,
                        "ne": False,
                        "cinema": False,
                        "seconds": 151.589,
                        "paritySummary": {
                            "errors": 0,
                            "warns": 0,
                            "resets": 1
                        },
                        "stars": 9.13,
                        "maxScore": 1467515,
                        "label": "APEX",
                        "blStars": 10.09,
                        "environment": "DefaultEnvironment"
                    }
                ],
                "downloadURL": "https://r2cdn.beatsaver.com/fd34b0279836820254c31552c5753291acbcbb95.zip",
                "coverURL": "https://eu.cdn.beatsaver.com/fd34b0279836820254c31552c5753291acbcbb95.jpg",
                "previewURL": "https://eu.cdn.beatsaver.com/fd34b0279836820254c31552c5753291acbcbb95.mp3"
            }
        ],
        "curator": {
            "id": 4284639,
            "name": "pkdan",
            "hash": "5e6d07927abb00000681e8ee",
            "avatar": "https://cdn.beatsaver.com/avatar/040e43a2c966d40aeab0ed5d65f5c2ccc987ded6.png",
            "type": "DISCORD",
            "admin": False,
            "curator": False,
            "seniorCurator": False,
            "curatorTab": True,
            "verifiedMapper": True,
            "playlistUrl": "https://api.beatsaver.com/users/id/4284639/playlist"
        },
        "curatedAt": "2022-05-29T13:05:01.932483Z",
        "createdAt": "2021-01-14T11:56:39.803Z",
        "updatedAt": "2022-05-29T13:05:01.932483Z",
        "lastPublishedAt": "2021-01-14T11:56:39.803Z",
        "tags": [
            "dance",
            "electronic",
            "balanced",
            "speed"
        ],
        "bookmarked": False,
        "declaredAi": "None",
        "blRanked": True,
        "blQualified": False
    }
}
    return response

def test_singleMapCall():
    responseJSON = beatSaverAPICaller.BeatSaverAPICaller.singleMapCall('57c2')
    ## header
    assert responseJSON['id'] == '57c2'
    assert responseJSON['name'] == 'Rockefeller Street (Nightcore) -  Getter Jaani'
    assert responseJSON['versions'][0]['hash'] == 'b8c98ffc598703aadb4a3cb921d2830d270b57a5'

    ## metdadata
    assert responseJSON['metadata']['songName'] == 'Rockefeller Street (Nightcore)'
    assert responseJSON['metadata']['songAuthorName'] == 'Getter Jaani'
    assert responseJSON['metadata']['levelAuthorName'] == 'RinkuSenpai'
    assert responseJSON['metadata']['bpm'] == 162.5
    assert responseJSON['metadata']['duration'] == 145
    assert responseJSON['ranked'] == True
    assert responseJSON['qualified'] == False
    assert responseJSON['uploaded'] == '2019-07-18T21:40:09.204Z'
    assert responseJSON['tags'] == ['pop']
    
    ## links
    assert responseJSON['versions'][0]['downloadURL'] == 'https://r2cdn.beatsaver.com/b8c98ffc598703aadb4a3cb921d2830d270b57a5.zip'
    assert responseJSON['versions'][0]['coverURL'] == 'https://eu.cdn.beatsaver.com/b8c98ffc598703aadb4a3cb921d2830d270b57a5.jpg'
    assert responseJSON['versions'][0]['previewURL'] == 'https://eu.cdn.beatsaver.com/b8c98ffc598703aadb4a3cb921d2830d270b57a5.mp3'

    ## levels
    level0 = responseJSON['versions'][0]['diffs'][0]
    assert level0['difficulty'] == 'Hard'
    assert level0['characteristic'] == 'Standard'
    assert level0['njs'] == 13
    assert level0['nps'] == 3.884
    assert level0['stars'] == 3.4
    assert level0['chroma'] == False
    assert level0['me'] == False
    assert level0['ne'] == False
    assert level0['cinema'] == False

    level1 = responseJSON['versions'][0]['diffs'][1]
    assert level1['difficulty'] == 'Expert'
    assert level1['characteristic'] == 'Standard'
    assert level1['njs'] == 17
    assert level1['nps'] == 5.053
    assert level1['stars'] == 3.7
    assert level1['chroma'] == False
    assert level1['me'] == False
    assert level1['ne'] == False
    assert level1['cinema'] == False

def test_singleMapCall_Exception():
    with pytest.raises(beatSaverAPICaller.NotBeatSaverMap):
        beatSaverAPICaller.BeatSaverAPICaller.singleMapCall('')

def test_splitListToChunks():
    inputData = [i for i in range(17)]

    beatSaverAPICaller.BeatSaverAPICaller.MULTIPLE_MAP_CALL_LIST_LENGTH = 5    
    assert beatSaverAPICaller.BeatSaverAPICaller.splitListToChunks(inputData) == [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16]]

    beatSaverAPICaller.BeatSaverAPICaller.MULTIPLE_MAP_CALL_LIST_LENGTH = 4    
    assert beatSaverAPICaller.BeatSaverAPICaller.splitListToChunks(inputData) == [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15], [16]]

    beatSaverAPICaller.BeatSaverAPICaller.MULTIPLE_MAP_CALL_LIST_LENGTH = 17    
    assert beatSaverAPICaller.BeatSaverAPICaller.splitListToChunks(inputData) == [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]]

def test_multipleMapsCall(multipleCallExpected):
    responseJSON = beatSaverAPICaller.BeatSaverAPICaller.multipleMapsCall(['57c2', '12b62'])
    responseJSON['57c2'].pop('stats')    
    responseJSON['12b62'].pop('stats')
    print(responseJSON['57c2'])
    assert responseJSON == multipleCallExpected