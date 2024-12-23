import pytest
import filterMapCacheDecorators

@pytest.fixture
def mockBaseNode():
    cache = {
        'longString': 'inabakumori challenge expert tech lawless hard lagtrain pop hickeychan expertplus vocaloid', 
        'length': 252, 
        'bpm': 147.0, 
        'mods': {'ne', 'chroma'}, 
        'nps': (3.862, 4.101), 
        'njs': 16.0,
        'stars': '?', 
        'rankedState': set(['Graveyard'])
    }
    return filterMapCacheDecorators.BaseCacheNode(cache)

@pytest.mark.parametrize('inputCacheValue, inputRequiredValue, expected', [
    ((1, 3), (0, 3), False), ((1, 3), (2, 3), True), ((0, 4), (2, 3), True), ((2, 3), (2, 3), True), ((2, 3), (3, 2), True), 
    ((2, 3), (0, 4), False), ((0, 2), (0, 3), False),(2, (0, 3), True), (-2, (0, 3), False), (0, (0, 3), True), (3, (0, 3), True),
    ('test', 'test', True), ('test', '', False), ('', '', True)])
def test__checkRangeOrStr(inputCacheValue, inputRequiredValue, expected):
    assert filterMapCacheDecorators.CheckRangeOrStringDecorator._checkRangeOrStr(None, inputCacheValue, inputRequiredValue) == expected

@pytest.mark.parametrize('inputData, expected', [('chall', True), ('test', False), ('.....', True), ('(pop|hard|eeeasy)', True)])
def test_CheckLongString(inputData, expected, mockBaseNode):
    mockBaseNode = filterMapCacheDecorators.CheckLongStringDecorator(mockBaseNode, 'longString', inputData)
    assert mockBaseNode.checkCriteria() == expected

@pytest.mark.parametrize('inputData, expected', [('252', True), ('253', False), ('nasjidbasud', False), 
    ((100, 300), True), ((100, 101), False), ((100, 252.99), False)])
def test_CheckRangeOrString_oneValueCached(inputData, expected, mockBaseNode):
    #'length': 252
    mockBaseNode = filterMapCacheDecorators.CheckRangeOrStringDecorator(mockBaseNode, 'length', inputData) == expected

@pytest.mark.parametrize('inputData, expected', [((3, 5), True), ((3.5, 4.2), True), ((3.5, 4.101), True), ((3.5, 4.1), False), ((3.862, 10), True), 
    ((1, 2), False), ((3, 10), False), ((1, 4), False), ((6, 10), False)])
def test_CheckRangeOrString_RangeCached(inputData, expected, mockBaseNode):
    #'nps': (3.862, 4.101)
    mockBaseNode = filterMapCacheDecorators.CheckRangeOrStringDecorator(mockBaseNode, 'nps', inputData) == expected

@pytest.mark.parametrize('inputData, expected', [(['ne'], True), (['chroma'], True), (['ne', 'chroma'], True), 
    ([], False), (['me'], False), (['me', 'chroma'], True)])
def test_CheckLongString(inputData, expected, mockBaseNode):
    #'mods': {'ne', 'chroma'}
    mockBaseNode = filterMapCacheDecorators.CheckValueSetDecorator(mockBaseNode, 'mods', inputData)
    assert mockBaseNode.checkCriteria() == expected

@pytest.mark.parametrize('inputDataList, expected', [
        ([('longString', 'expert')], True),
        ([('longString', 'expert'), ('length', (250, 270)), ('njs', 16)], True),
        ([('longString', 'expert'), ('length', (250, 270)), ('njs', (12, 13))], False),
        ([('longString', 'tests'), ('length', (250, 270)), ('njs', 16)], False),
        ([('length', (250, 270)), ('njs', 16), ('nps', (3.9, 4.0)), ('stars', '?')], True), 
        ([('length', (250, 270)), ('njs', 16), ('nps', (3.9, 4.8)), ('stars', '?')], False), 
        ([('rankedState', ['Graveyard', 'Ranked']), ('longString', 'vocal'), ('length', (250, 270)), ('njs', 16), ('mods', ['chroma'])], True),
    ])
def test_decoratorChaining(inputDataList, expected, mockBaseNode):
    decoratorsDict = {
        'longString': filterMapCacheDecorators.CheckLongStringDecorator,
        'rankedState': filterMapCacheDecorators.CheckValueSetDecorator,
        'mods': filterMapCacheDecorators.CheckValueSetDecorator
    }

    for criteriaTuple in inputDataList:
        key, criteria = criteriaTuple
        decorator = decoratorsDict.get(key, filterMapCacheDecorators.CheckRangeOrStringDecorator)
        mockBaseNode = decorator(mockBaseNode, key, criteria)
    
    assert mockBaseNode.checkCriteria() == expected

        
