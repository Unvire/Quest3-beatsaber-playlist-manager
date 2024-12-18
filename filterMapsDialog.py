import sys, os
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QCheckBox
from PyQt5 import uic

from beatSaberMap import BeatSaberMap


class FilterMapsDialog(QDialog):
    def __init__(self, mapsCacheList:list[dict]):
        super().__init__()
        uiFilePath = os.path.join(os.getcwd(), 'ui', 'searchMapsDialog.ui')
        uic.loadUi(uiFilePath, self)

        self.rankedStateSelectionSet = set()
        self.modsSelectionSet = set()

        self.lengthEdit.editingFinished.connect(lambda: self._validateEdit(self.lengthEdit, 'numeric'))
        self.bpmEdit.editingFinished.connect(lambda: self._validateEdit(self.bpmEdit, 'numeric'))
        self.npsEdit.editingFinished.connect(lambda: self._validateEdit(self.npsEdit, 'numeric'))
        self.njsEdit.editingFinished.connect(lambda: self._validateEdit(self.njsEdit, 'numeric'))
        self.starsEdit.editingFinished.connect(lambda: self._validateEdit(self.starsEdit, 'numericOrStr'))
        self.uploadedEdit.editingFinished.connect(lambda: self._validateEdit(self.uploadedEdit, 'date'))

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
    
    def _validateEdit(self, editHandle:QLineEdit, editType:str):
        print(editHandle.text(), editType)
    
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
    items = [{}, {}]
    app = QApplication(sys.argv)
    window = FilterMapsDialog(items)
    window.show()
    sys.exit(app.exec_())