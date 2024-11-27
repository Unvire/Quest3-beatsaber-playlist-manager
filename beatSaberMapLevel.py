class BeatSaberMapLevel():
    def __init__(self, level:dict):
        self.difficulty = level['difficulty']
        self.characteristic = level['characteristic']
        self.njs = level['njs']
        self.nps = level['nps']
        self.stars = level['stars']
        allModsNames = ['chroma', 'me', 'ne', 'cinema']
        self.requiredMods = [modName for modName in allModsNames if level[modName]]
    
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
    
    a = BeatSaberMapLevel(mockDict)
    print(a)