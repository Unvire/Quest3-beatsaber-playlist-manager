import sys, os
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QCheckBox
from PyQt5 import uic


class SelectItemsDialog(QDialog):
    def __init__(self, items):
        super().__init__()
        uiFilePath = os.path.join(os.getcwd(), 'ui', 'deletePlaylistsDialog.ui')
        uic.loadUi(uiFilePath, self)
        
        if not self.scrollAreaWidgetContents.layout():
            layout = QVBoxLayout(self.scrollAreaWidgetContents)
            self.scrollAreaWidgetContents.setLayout(layout)

        self.checkboxes = []
        for item in items:
            checkbox = QCheckBox(item)
            self.checkboxes.append(checkbox)
            self.scrollAreaWidgetContents.layout().addWidget(checkbox)
        
        self.cancelButton.clicked.connect(self.reject)
        self.deleteButton.clicked.connect(self.accept)

    def getSelectedItems(self):
        selectedItems = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]
        return selectedItems


if __name__ == '__main__':
    items = [f'Element {i + 1}' for i in range(100)]
    app = QApplication(sys.argv)
    window = SelectItemsDialog(items)
    window.show()
    sys.exit(app.exec_())