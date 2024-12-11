import pytest
import beatSaverAPICaller

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
    level = responseJSON['versions'][0]['diffs'][0]
    assert level['difficulty'] == 'Hard'
    assert level['characteristic'] == 'Standard'
    assert level['njs'] == 13
    assert level['nps'] == 3.884
    assert level['stars'] == 3.4
    assert level['chroma'] == False
    assert level['me'] == False
    assert level['ne'] == False
    assert level['cinema'] == False

    level = responseJSON['versions'][0]['diffs'][1]
    assert level['difficulty'] == 'Expert'
    assert level['characteristic'] == 'Standard'
    assert level['njs'] == 17
    assert level['nps'] == 5.053
    assert level['stars'] == 3.7
    assert level['chroma'] == False
    assert level['me'] == False
    assert level['ne'] == False
    assert level['cinema'] == False

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

def test_multipleMapsCall():
    responseJSON = beatSaverAPICaller.BeatSaverAPICaller.multipleMapsCall(['57c2', '12b62'])
    assert list(responseJSON.keys()) == ['57c2', '12b62']
    
    ## test first map
    map1 = responseJSON['57c2']
    assert map1['id'] == '57c2'
    assert map1['name'] == 'Rockefeller Street (Nightcore) -  Getter Jaani'
    assert map1['versions'][0]['hash'] == 'b8c98ffc598703aadb4a3cb921d2830d270b57a5'

    ## metdadata
    assert map1['metadata']['songName'] == 'Rockefeller Street (Nightcore)'
    assert map1['metadata']['songAuthorName'] == 'Getter Jaani'
    assert map1['metadata']['levelAuthorName'] == 'RinkuSenpai'
    assert map1['metadata']['bpm'] == 162.5
    assert map1['metadata']['duration'] == 145
    assert map1['ranked'] == True
    assert map1['qualified'] == False
    assert map1['uploaded'] == '2019-07-18T21:40:09.204Z'
    assert map1['tags'] == ['pop']
    
    ## links
    assert map1['versions'][0]['downloadURL'] == 'https://r2cdn.beatsaver.com/b8c98ffc598703aadb4a3cb921d2830d270b57a5.zip'
    assert map1['versions'][0]['coverURL'] == 'https://eu.cdn.beatsaver.com/b8c98ffc598703aadb4a3cb921d2830d270b57a5.jpg'
    assert map1['versions'][0]['previewURL'] == 'https://eu.cdn.beatsaver.com/b8c98ffc598703aadb4a3cb921d2830d270b57a5.mp3'

    ## levels
    level = map1['versions'][0]['diffs'][0]
    assert level['difficulty'] == 'Hard'
    assert level['characteristic'] == 'Standard'
    assert level['njs'] == 13
    assert level['nps'] == 3.884
    assert level['stars'] == 3.4
    assert level['chroma'] == False
    assert level['me'] == False
    assert level['ne'] == False
    assert level['cinema'] == False

    level = map1['versions'][0]['diffs'][1]
    assert level['difficulty'] == 'Expert'
    assert level['characteristic'] == 'Standard'
    assert level['njs'] == 17
    assert level['nps'] == 5.053
    assert level['stars'] == 3.7
    assert level['chroma'] == False
    assert level['me'] == False
    assert level['ne'] == False
    assert level['cinema'] == False

    ## test second map
    map2 = responseJSON['12b62']
    assert map2['id'] == '12b62'
    assert map2['name'] == 'USAO - Climax [Ranked]'
    assert map2['versions'][0]['hash'] == 'fd34b0279836820254c31552c5753291acbcbb95'

    ## metdadata
    assert map2['metadata']['songName'] == 'Climax'
    assert map2['metadata']['songAuthorName'] == 'USAO'
    assert map2['metadata']['levelAuthorName'] == 'Timbo'
    assert map2['metadata']['bpm'] == 190
    assert map2['metadata']['duration'] == 156
    assert map2['ranked'] == True
    assert map2['qualified'] == False
    assert map2['uploaded'] == '2021-01-14T11:56:39.803Z'
    assert map2['tags'] == ['dance', 'electronic', 'balanced', 'speed']
    
    ## links
    assert map2['versions'][0]['downloadURL'] == 'https://r2cdn.beatsaver.com/fd34b0279836820254c31552c5753291acbcbb95.zip'
    assert map2['versions'][0]['coverURL'] == 'https://eu.cdn.beatsaver.com/fd34b0279836820254c31552c5753291acbcbb95.jpg'
    assert map2['versions'][0]['previewURL'] == 'https://eu.cdn.beatsaver.com/fd34b0279836820254c31552c5753291acbcbb95.mp3'

    ## levels
    level = map2['versions'][0]['diffs'][0]
    assert level['difficulty'] == 'Easy'
    assert level['characteristic'] == 'Standard'
    assert level['njs'] == 14
    assert level['nps'] == 3.622
    assert level['stars'] == 2.64
    assert level['chroma'] == False
    assert level['me'] == False
    assert level['ne'] == False
    assert level['cinema'] == False

    level = map2['versions'][0]['diffs'][1]
    assert level['difficulty'] == 'Normal'
    assert level['characteristic'] == 'Standard'
    assert level['njs'] == 16
    assert level['nps'] == 5.37
    assert level['stars'] == 3.44
    assert level['chroma'] == False
    assert level['me'] == False
    assert level['ne'] == False
    assert level['cinema'] == False

    level = map2['versions'][0]['diffs'][2]
    assert level['difficulty'] == 'Hard'
    assert level['characteristic'] == 'Standard'
    assert level['njs'] == 18
    assert level['nps'] == 6.723
    assert level['stars'] == 5.19
    assert level['chroma'] == False
    assert level['me'] == False
    assert level['ne'] == False
    assert level['cinema'] == False

    level = map2['versions'][0]['diffs'][3]
    assert level['difficulty'] == 'Expert'
    assert level['characteristic'] == 'Standard'
    assert level['njs'] == 19
    assert level['nps'] == 9.823
    assert level['stars'] == 7.48
    assert level['chroma'] == False
    assert level['me'] == False
    assert level['ne'] == False
    assert level['cinema'] == False

    level = map2['versions'][0]['diffs'][4]
    assert level['difficulty'] == 'ExpertPlus'
    assert level['characteristic'] == 'Standard'
    assert level['njs'] == 21
    assert level['nps'] == 10.575
    assert level['stars'] == 9.13
    assert level['chroma'] == False
    assert level['me'] == False
    assert level['ne'] == False
    assert level['cinema'] == False
