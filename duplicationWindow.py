from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QStyleFactory
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt


class duplWin(QWidget):

    def __init__(self, name, dM):
        super().__init__()
        self.Arial12Font = QFont('Arial', 12)
        self.Arial12Font.setBold(True)
        self.Arial12Font.setPixelSize(16)
        self.Arial12FontNB = QFont('Arial', 12)
        self.Arial12FontNB.setPixelSize(16)
        self.setWindowIcon(QIcon('Settings/icon.png'))
        self.setFixedSize(400, 100)
        self.setWindowTitle('Duplicating ' + name)
        self.name = name
        if dM:
            self.setStyleSheet(open('Settings/darkModeSS').read())
            self.setStyle(QStyleFactory.create('Windows'))
        else:
            self.setStyle(QStyleFactory().create('Fusion'))
            self.setStyleSheet('{background-color: #f0f0ed;} QAbstractItemView {border: 2px solid darkgray;selection-background-color: lightgray;}')
        self.show()
        self.initUi()

    def initUi(self):
        self.nameLabel = QLabel('Copy name', self)
        self.nameLabel.setFont(self.Arial12FontNB)
        self.nameLabel.move(10, 10)
        self.nameLabel.resize(80, 20)
        self.nameLabel.show()

        self.nameTB = QLineEdit(self.name, self)
        self.nameTB.move(100, 10)
        self.nameTB.resize(290, 20)
        self.nameTB.show()

        self.confirmButton = QPushButton('Confirm', self)
        self.confirmButton.move(10, 40)
        self.confirmButton.resize(380, 23)
        self.confirmButton.show()

        self.confirmLabel = QLabel(self)
        self.confirmLabel.move(10, 70)
        self.confirmLabel.resize(380, 20)
        self.confirmLabel.setFont(self.Arial12Font)
        self.confirmLabel.setAlignment(Qt.AlignCenter)
        self.confirmLabel.show()
