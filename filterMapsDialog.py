from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import uic

import sys, os, re
from beatSaberPlaylist import BeatSaberPlaylist
from filterMapCacheDecorators import BaseCacheNode, CheckLongString, CheckRangeOrString, CheckValueSet


class FilterMapsDialog(QDialog):
    FLOAT_PATTERN = '(-?\d*(?:\.\d+)?)?'
    RANGE_PATTERN = f'^\[{FLOAT_PATTERN};{FLOAT_PATTERN}]$'

    def __init__(self, playlist:BeatSaberPlaylist, uiFilePath=''):
        super().__init__()
        if not uiFilePath:
            uiFilePath = os.path.join(os.getcwd(), 'ui', 'searchMapsDialog.ui')
        uic.loadUi(uiFilePath, self)

        self.previousSearchParameters = self._defaultPreviousSearchParameters()
        self.playlist = playlist

        self.rankedStateSelectionSet = set()
        self.modsSelectionSet = set()

        self.graveyardCheckbox.toggled.connect(lambda state: self._rankedStateCheckboxToggled(state, 'Graveyard'))
        self.qualifiedCheckbox.toggled.connect(lambda state: self._rankedStateCheckboxToggled(state, 'Qualified'))
        self.rankedCheckbox.toggled.connect(lambda state: self._rankedStateCheckboxToggled(state, 'Ranked'))
        
        self.noModsCheckbox.toggled.connect(lambda state: self._modsCheckboxToggled(state, 'No mods'))
        self.chromaCheckbox.toggled.connect(lambda state: self._modsCheckboxToggled(state, 'chroma'))
        self.neCheckbox.toggled.connect(lambda state: self._modsCheckboxToggled(state, 'ne'))
        self.meCheckbox.toggled.connect(lambda state: self._modsCheckboxToggled(state, 'me'))
        self.cinemaCheckbox.toggled.connect(lambda state: self._modsCheckboxToggled(state, 'cinema'))

        self.clearSearchParametersButton.clicked.connect(self.clearSearchParameters)
        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
    
    def setPreviousSearchParameters(self, previousSearchParameters:dict):
        self.previousSearchParameters = previousSearchParameters
        self._setWidgets(previousSearchParameters)
    
    def clearSearchParameters(self):
        parametersDict = self._defaultPreviousSearchParameters()
        self._setWidgets(parametersDict)
    
    def _setWidgets(self, parametersDict:dict):
        def valueToString(value):
            if isinstance(value, tuple):
                minVal, maxVal = value
                minVal = '' if minVal in (float('inf'), float('-inf')) else minVal                
                maxVal = '' if maxVal in (float('inf'), float('-inf')) else maxVal
                return f'[{minVal};{maxVal}]'
            return f'{value}'

        self.parametersEdit.setText(parametersDict['longString'])
        
        self.lengthEdit.setText(valueToString(parametersDict['length']))        
        self.bpmEdit.setText(valueToString(parametersDict['bpm']))        
        self.npsEdit.setText(valueToString(parametersDict['nps']))        
        self.njsEdit.setText(valueToString(parametersDict['njs']))        
        self.starsEdit.setText(valueToString(parametersDict['stars']))

        self.rankedStateSelectionSet = parametersDict['rankedState']
        self.graveyardCheckbox.setChecked('Graveyard' in self.rankedStateSelectionSet)
        self.qualifiedCheckbox.setChecked('Qualified' in self.rankedStateSelectionSet)
        self.rankedCheckbox.setChecked('Ranked' in self.rankedStateSelectionSet)

        self.modsSelectionSet = parametersDict['mods']
        self.noModsCheckbox.setChecked('No mods' in self.modsSelectionSet)
        self.chromaCheckbox.setChecked('chroma' in self.modsSelectionSet)
        self.neCheckbox.setChecked('ne' in self.modsSelectionSet)
        self.meCheckbox.setChecked('me' in self.modsSelectionSet)
        self.cinemaCheckbox.setChecked('cinema' in self.modsSelectionSet)
    
    def _defaultPreviousSearchParameters(self) -> dict:
        default = {
            'longString': '', 
            'length': '', 
            'bpm': '',
            'nps': '',
            'njs': '',
            'stars': '', 
            'rankedState': set(), 
            'mods': set()
        }
        return default
        
    def getHideIndexesList(self) -> list[int]:
        longStringPattern = self.parametersEdit.text()
        requiredLength = self._extractRangeValuesFromString(self.lengthEdit.text())
        requiredBpm = self._extractRangeValuesFromString(self.bpmEdit.text())
        requiredNps = self._extractRangeValuesFromString(self.npsEdit.text())
        requiredNjs = self._extractRangeValuesFromString(self.njsEdit.text())
        requiredStars = self._extractRangeValuesFromString(self.starsEdit.text())
        requiredRankedStates = self.rankedStateSelectionSet
        requiredMods = self.modsSelectionSet

        return self._filterMaps(longStringPattern=longStringPattern, requiredLength=requiredLength, requiredBpm=requiredBpm, requiredNps=requiredNps,
                                requiredNjs=requiredNjs, requiredStars=requiredStars, requiredRankedStates=requiredRankedStates, requiredMods=requiredMods)

    def getPreviousSearchParameters(self) -> dict:
        return self.previousSearchParameters
    
    def _filterMaps(self, longStringPattern:str='', requiredLength:tuple[float, float]|str=None, requiredBpm:tuple[float, float]|str=None, 
                    requiredNps:tuple[float, float]|str=None, requiredNjs:tuple[float, float]|str=None, requiredStars:tuple[float, float]|str=None, 
                    requiredRankedStates:list[str]=None, requiredMods:list[str]=None) -> list[int]:
        
        decoratorsDict = {
            'longString': CheckLongString,
            'rankedState': CheckValueSet,
            'mods': CheckValueSet
        }
        keyNames = ['longString', 'length', 'bpm', 'nps', 'njs', 'stars', 'rankedState', 'mods']
        allCriterias = [longStringPattern, requiredLength, requiredBpm, requiredNps, requiredNjs, requiredStars, requiredRankedStates, requiredMods]
        
        self.previousSearchParameters = self._defaultPreviousSearchParameters()
        criteriaTuples = []
        for keyName, criteria in zip(keyNames, allCriterias):
            if criteria:
                self.previousSearchParameters[keyName] = criteria
                criteriaTuples.append((keyName, criteria))

        result = []
        for i, song in enumerate(self.playlist):
            songNode = BaseCacheNode(song.getCacheData())

            # chain filtering decorators
            for key, criteria in criteriaTuples:
                decorator = decoratorsDict.get(key, CheckRangeOrString)
                songNode = decorator(songNode, key, criteria) 
            
            if not songNode.checkCriteria():
                result.append(i)
        return result
    
    def _extractRangeValuesFromString(self, value:str) -> str | tuple[float, float]:
        value = value.strip().replace(' ', '')        
        if re.search(FilterMapsDialog.RANGE_PATTERN, value):
            minVal, maxVal = value[1:-1].split(';')
            minVal = float(minVal) if minVal else float('-inf')
            maxVal = float(maxVal) if maxVal else float('inf')
            return minVal, maxVal
        return value

    def _rankedStateCheckboxToggled(self, state:bool, value:str):
        if state:
            self.rankedStateSelectionSet.add(value)
        else:
            self.rankedStateSelectionSet.discard(value)
        
        selectedStates = ', '.join(sorted(list(self.rankedStateSelectionSet)))
        selectedStates = 'Any' if not selectedStates else selectedStates
        self.rankedStateLabel.setText(f'Ranked state: {selectedStates}')
    
    def _modsCheckboxToggled(self, state:bool, value:str):
        modsDict = {
            'No mods': 'No mods',
            'chroma': 'Chroma',
            'ne': 'Noodle Extensions',
            'me': 'Mapping Extensions',
            'cinema': 'Cinema'
        }
        
        if state:
            self.modsSelectionSet.add(value)
        else:
            self.modsSelectionSet.discard(value)
        
        modsNames = [modsDict[val] for val in list(self.modsSelectionSet)]
        selectedStates = ', '.join(sorted(modsNames))
        selectedStates = 'Any' if not selectedStates else selectedStates
        self.modsLabel.setText(f'Mods: {selectedStates}')


if __name__ == '__main__':
    previousSearchParameters = {
            'longString': 'expert', 
            'length': 120, 
            'bpm': (120, 180), 
            'nps': 16, 
            'njs': 4, 
            'stars': '?', 
            'rankedState': set(['Ranked']), 
            'mods': set(['No mods', 'chroma'])
        }

    items = BeatSaberPlaylist()
    app = QApplication(sys.argv)
    window = FilterMapsDialog(items)
    window.show()
    window.setPreviousSearchParameters(previousSearchParameters)
    sys.exit(app.exec_())