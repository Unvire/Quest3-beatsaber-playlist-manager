import re

class BaseCacheNode:
    def __init__(self, cache:dict):
        self.cache = cache
        self.next = None
        self.criteria = None
    
    def checkCriteria(self) -> bool:
        return True

class AbstractCriteriaNode:
    def __init__(self, node:'BaseCacheNode|AbstractCriteriaNode'):
        self.cache = node.cache
        self.next = node
        self.criteria = None
    
    def checkCriteria(self) -> bool:
        pass

class CheckLongString(AbstractCriteriaNode):
    def __init__(self, node:'BaseCacheNode|AbstractCriteriaNode', cacheKey:str, pattern:str):
        super().__init__(node)
        self.cacheKey = cacheKey
        self.criteria = pattern
    
    def checkCriteria(self) -> bool:
        result = re.match(self.criteria, self.cache[self.cacheKey])
        if not result:
            return False
        return self.next.checkCriteria()

class CheckRangeOrString(AbstractCriteriaNode):
    def __init__(self, node:'BaseCacheNode|AbstractCriteriaNode', cacheKey:str, criteria:str):
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

if __name__ == '__main__':
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
    