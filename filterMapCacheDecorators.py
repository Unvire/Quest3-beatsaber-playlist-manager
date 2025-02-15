import re

class BaseCacheNode:
    def __init__(self, cache:dict):
        self.cache = cache
        self.next = None
        self.criteria = None
    
    def checkCriteria(self) -> bool:
        return True

class AbstractCriteriaDecorator:
    def __init__(self, node:'BaseCacheNode|AbstractCriteriaDecorator'):
        self.cache = node.cache
        self.next = node
        self.criteria = None
    
    def checkCriteria(self) -> bool:
        pass

class CheckLongStringDecorator(AbstractCriteriaDecorator):
    def __init__(self, node:'BaseCacheNode|AbstractCriteriaDecorator', cacheKey:str, pattern:str):
        super().__init__(node)
        self.cacheKey = cacheKey
        self.pattern = pattern
    
    def checkCriteria(self) -> bool:
        longString = self.cache[self.cacheKey]
        result = re.search(self.pattern, longString)
        if not result:
            return False
        return self.next.checkCriteria()

class CheckRangeOrStringDecorator(AbstractCriteriaDecorator):
    def __init__(self, node:'BaseCacheNode|AbstractCriteriaDecorator', cacheKey:str, criteria:str|tuple[float, float]):
        super().__init__(node)
        self.cacheKey = cacheKey
        self.criteria = criteria

    def checkCriteria(self) -> bool:
        result = self._checkRangeOrStr(self.cache[self.cacheKey], self.criteria)
        if not result:
            return False
        return self.next.checkCriteria()

    def _checkRangeOrStr(self, cacheVal:str|tuple[float, float]|float, requiredValue:str|tuple[float, float]) -> bool:
        if isinstance(requiredValue, tuple):
            requiredMinVal, requiredMaxVal = requiredValue
            if isinstance(cacheVal, tuple):
                minVal, maxVal = cacheVal
                return requiredMinVal >= minVal and requiredMaxVal <= maxVal
            elif isinstance(cacheVal, float) or isinstance(cacheVal, int):
                return requiredMinVal <= cacheVal <= requiredMaxVal
        return requiredValue == cacheVal

class CheckValueSetDecorator(AbstractCriteriaDecorator):
    def __init__(self, node:'BaseCacheNode|AbstractCriteriaDecorator', cacheKey:str, criteria:list[str]):
        super().__init__(node)
        self.cacheKey = cacheKey
        self.criteria = criteria
    
    def checkCriteria(self) -> bool:
        cachedSet = self.cache[self.cacheKey]
        criteriaSet = set(self.criteria)
        result = cachedSet & criteriaSet
        if not result:
            return False
        return self.next.checkCriteria()

if __name__ == '__main__':
    cache = {
        'longString': 'inabakumori challenge expert tech lawless hard lagtrain pop hickeychan expertplus vocaloid', 
        'length': 252, 
        'bpm': 147.0, 
        'mods': {'ne', 'chroma'}, 
        'nps': (3.862, 4.101), 
        'njs': 16.0, 
        'stars': '?', 
        'rankedState': 'Graveyard'
    }
    
    cacheNode = BaseCacheNode(cache)
    print(cacheNode.checkCriteria()) #Default Case is True 

    node = CheckLongStringDecorator(cacheNode, 'longString', 'expert')
    node = CheckRangeOrStringDecorator(node, 'length', (250, 270))
    print(node.checkCriteria()) # 2 criteria checked, both matching so result is True

    node = CheckLongStringDecorator(cacheNode, 'longString', 'expert')
    node = CheckRangeOrStringDecorator(node, 'length', (250, 210))
    print(node.checkCriteria()) # 2 criteria checked, length is no matching so result is False

    node = CheckLongStringDecorator(cacheNode, 'longString', 'test')
    node = CheckRangeOrStringDecorator(node, 'length', (250, 270))
    print(node.checkCriteria()) # 2 criteria checked, longstring is no matching so result is False

    node = CheckLongStringDecorator(cacheNode, 'longString', 'tech')
    node = CheckRangeOrStringDecorator(node, 'length', (250, 270))
    node = CheckLongStringDecorator(node, 'longString', 'challenge')
    node = CheckRangeOrStringDecorator(node, 'length', (250, 270))
    node = CheckLongStringDecorator(node, 'longString', 'expert')
    node = CheckRangeOrStringDecorator(node, 'length', (250, 270))
    node = CheckLongStringDecorator(node, 'longString', 'tech')
    node = CheckRangeOrStringDecorator(node, 'length', (250, 270))
    print(node.checkCriteria()) # True, criteria can be chained without hard coded limit