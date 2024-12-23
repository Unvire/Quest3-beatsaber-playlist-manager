from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit
from PyQt5 import uic

import sys, os, re
from beatSaberMap import BeatSaberMap
from beatSaberPlaylist import BeatSaberPlaylist


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

        return self._filterMaps(playlist=self.playlist, longStringPattern=longStringPattern, requiredLength=requiredLength, requiredBpm=requiredBpm, requiredNps=requiredNps,
                                requiredNjs=requiredNjs, requiredStars=requiredStars, requiredRankedStates=requiredRankedStates, requiredMods=requiredMods)
    
    def _filterMaps(self, longStringPattern:str='', requiredLength:tuple[float, float]|str=None, requiredBpm:tuple[float, float]|str=None, 
                    requiredNps:tuple[float, float]|str=None, requiredNjs:tuple[float, float]|str=None, requiredStars:tuple[float, float]|str=None, 
                    requiredRankedStates:list[str]=None, requiredMods:list[str]=None) -> list[int]:
        result = []
        for i, song in enumerate(self.playlist):
            criteriaMatched = []
            cache = song.getCacheData()

            criteriaMatched.append(bool(re.match(longStringPattern, cache['longString'])))
            criteriaMatched.append(self._checkRangeOrStr(cache['length'], requiredLength))
            criteriaMatched.append(self._checkRangeOrStr(cache['bpm'], requiredBpm))
            criteriaMatched.append(self._checkRangeOrStr(cache['nps'], requiredNps))
            criteriaMatched.append(self._checkRangeOrStr(cache['njs'], requiredNjs))            
            criteriaMatched.append(self._checkRangeOrStr(cache['stars'], requiredStars))
            
            if requiredRankedStates:
                criteriaMatched.append(cache['rankedState'] in requiredRankedStates)
            if requiredMods:
                requiredMods = set(requiredMods)
                criteriaMatched.append(not requiredMods or bool(cache['mods'] & requiredMods))

            if not all(criteriaMatched):
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