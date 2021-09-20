from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QStyleFactory
from PyQt5.QtGui import QIcon, QFont
from webbrowser import open as op


class addToken(QWidget):

    def __init__(self, dM):
        super().__init__()
        self.setWindowTitle('Formatting token window')
        icon = QIcon('Settings/icon.png')
        self.setWindowIcon(icon)
        self.setFixedSize(260, 70)
        self.arial12Bold = QFont('Arial', 12)
        self.arial12Bold.setBold(True)
        self.show()
        '''if dM:
            self.setStyleSheet(open('Settings/darkModeSS').read())
            self.setStyle(QStyleFactory.create('Fusion'))
        else:
            self.setStyle(QStyleFactory().create('Fusion'))
            self.setStyleSheet('{background-color: #f0f0ed;} QAbstractItemView {border: 2px solid darkgray;selection-background-color: lightgray;}')'''
        self.initUI()

    def initUI(self):
        self.tokComB = QComboBox(self)
        self.tokComB.move(10, 10)
        self.tokComB.resize(160, 20)
        items = ['%b', '%c', '%a', '%t', '%B', '%C', '%A', '%T', '%s', '%%', '%n']
        self.tokComB.addItems(items)
        self.tokComB.show()

        self.confButton = QPushButton('Add token', self)
        self.confButton.move(180, 10)
        self.confButton.resize(75, 20)
        self.confButton.show()

        self.wikiButton = QPushButton('WIKI', self)
        self.wikiButton.move(10, 40)
        self.wikiButton.resize(240, 20)
        self.wikiButton.setFont(self.arial12Bold)
        self.wikiButton.clicked.connect(self.openWiki)
        self.wikiButton.show()

    def openWiki(self):
        op('https://github.com/ErisApps/HitScoreVisualizer#format-tokens')
