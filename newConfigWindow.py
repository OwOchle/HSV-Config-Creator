from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QStyleFactory
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt


class newConf(QWidget):

    def __init__(self, dM):
        super().__init__()
        self.setFixedSize(400, 100)
        self.arial12 = QFont('Arial', 12)
        icon = QIcon('Settings/icon.png')
        self.setWindowIcon(icon)
        self.setWindowTitle('New config')
        if dM:
            self.setStyleSheet(open('Settings/darkModeSS').read())
            self.setStyle(QStyleFactory.create('Windows'))
        else:
            self.setStyle(QStyleFactory().create('Fusion'))
            self.setStyleSheet('{background-color: #f0f0ed;} QAbstractItemView {border: 2px solid darkgray;selection-background-color: lightgray;}')
        self.show()
        self.initUI()

    def initUI(self):
        self.nameLabel = QLabel('Config name', self)
        self.nameLabel.move(10, 10)
        self.nameLabel.resize(380, 20)
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.nameLabel.setFont(self.arial12)
        self.nameLabel.show()

        self.nameTB = QLineEdit(self)
        self.nameTB.move(10, 40)
        self.nameTB.resize(380, 20)
        self.nameTB.show()

        self.confirmButton = QPushButton('Confirm', self)
        self.confirmButton.move(10, 70)
        self.confirmButton.resize(380, 20)
        self.confirmButton.show()
