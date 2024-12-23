import pytest
import filterMapCacheDecorators

@pytest.fixture
def mockCache():
    cache = {
        'longString': 'inabakumori challenge expert tech lawless hard lagtrain pop hickeychan expertplus vocaloid', 
        'length': 252, 
        'bpm': 147.0, 
        'mods': {'ne', 'chroma'}, 
        'nps': (3.862, 4.101), 
        'njs': (16.0, 16.0), 
        'stars': '?', 
        'rankedState': 'Graveyard'
    }
    return cache

@pytest.mark.parametrize('inputCacheValue, inputRequiredValue, expected', [
    ((1, 3), (0, 3), False), ((1, 3), (2, 3), True), ((0, 4), (2, 3), True), ((2, 3), (2, 3), True), ((2, 3), (3, 2), True), ((2, 3), (0, 4), False), ((0, 2), (0, 3), False),
    (2, (0, 3), True), (-2, (0, 3), False), (0, (0, 3), True), (3, (0, 3), True),
    ('test', 'test', True), ('test', '', False), ('', '', True)])
def test__checkRangeOrStr(inputCacheValue, inputRequiredValue, expected):
    print(inputCacheValue, inputRequiredValue, expected)
    assert filterMapCacheDecorators.CheckRangeOrString._checkRangeOrStr(None, inputCacheValue, inputRequiredValue) == expected
