class BeatSaberMapLevel():
    def __init__(self, Data:dict):
        self.difficulty = Data.get('difficulty', '?')
        self.characteristic = Data.get('characteristic', '?')
        self.njs = Data.get('njs', '?')
        self.nps = Data.get('nps', '?')
        self.stars = Data.get('stars', '?')
        allModsNames = ['chroma', 'me', 'ne', 'cinema']
        self.requiredMods = ', '.join([modName for modName in allModsNames if Data[modName]])
    
    def __repr__(self):
        return f'{self.difficulty}[{self.characteristic}] {self.stars}*'


if __name__ == '__main__':
    mockDict = {
        'njs': 13,
        'offset': 0,
        'notes': 545,
        'bombs': 0,
        'obstacles': 8,
        'nps': 3.884,
        'length': 380,
        'characteristic': 'Standard',
        'difficulty': 'Hard',
        'events': 2247,
        'chroma': False,
        'me': False,
        'ne': False,
        'cinema': False,
        'seconds': 140.308,
        'paritySummary': {
            'errors': 73,
            'warns': 61,
            'resets': 0
        },
        'stars': 3.4,
        'maxScore': 494155,
        'environment': 'NiceEnvironment'
    }
    
    a = BeatSaberMapData(mockDict)
    print(a)