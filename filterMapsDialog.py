from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit
from PyQt5 import uic

import sys, os, re
from beatSaberMap import BeatSaberMap
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

        self.playlist = playlist

        self.rankedStateSelectionSet = set()
        self.modsSelectionSet = set()

        self.graveyardCheckbox.toggled.connect(lambda state: self._rankedStateCheckboxToggled(state, 'Graveyard'))
        self.qualifiedCheckbox.toggled.connect(lambda state: self._rankedStateCheckboxToggled(state, 'Qualified'))
        self.rankedCheckbox.toggled.connect(lambda state: self._rankedStateCheckboxToggled(state, 'Ranked'))
        
        self.noModsCheckbox.toggled.connect(lambda state: self._modsCheckboxToggled(state, 'No mods'))
        self.chromaCheckbox.toggled.connect(lambda state: self._modsCheckboxToggled(state, 'Chroma'))
        self.neCheckbox.toggled.connect(lambda state: self._modsCheckboxToggled(state, 'Noodle Extensions'))
        self.meCheckbox.toggled.connect(lambda state: self._modsCheckboxToggled(state, 'Mapping Extensions'))
        self.cinemaCheckbox.toggled.connect(lambda state: self._modsCheckboxToggled(state, 'Cinema'))

        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
    
    def getData(self) -> list[int]:
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


        criteriaTuples = [(keyName, criteria) for keyName, criteria in zip(keyNames, allCriterias) if criteria]
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
            self.rankedStateSelectionSet.remove(value)
        
        selectedStates = ', '.join(sorted(list(self.rankedStateSelectionSet)))
        selectedStates = 'Any' if not selectedStates else selectedStates
        self.rankedStateLabel.setText(f'Ranked state: {selectedStates}')
    
    def _modsCheckboxToggled(self, state:bool, value:str):
        modsDict = {
            'No mods': 'No mods',
            'Chroma': 'chroma',
            'Noodle Extensions': 'ne',
            'Mapping Extensions': 'me',
            'Cinema': 'cinema'
        }

        value = modsDict[value]
        if state:
            self.modsSelectionSet.add(value)
        else:
            self.modsSelectionSet.remove(value)
        
        selectedStates = ', '.join(sorted(list(self.modsSelectionSet)))
        selectedStates = 'Any' if not selectedStates else selectedStates
        self.modsLabel.setText(f'Mods: {selectedStates}')


if __name__ == '__main__':
    items = BeatSaberPlaylist()
    app = QApplication(sys.argv)
    window = FilterMapsDialog(items)
    window.show()
    sys.exit(app.exec_())