from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QSpinBox, QLineEdit, QDoubleSpinBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt


class cutJudgmentsConfig(QWidget):

    def __init__(self, conf, ind, judType, dM, new=False):
        super().__init__()
        self.conf = conf
        self.jud = self.conf[judType][ind]
        self.ind = ind
        self.new = new
        self.judType = judType
        self.arial12Bold = QFont('Arial', 12)
        self.arial12Bold.setBold(True)
        self.arial12Bold.setPixelSize(16)
        self.arial12 = QFont('Arial', 12)
        self.arial12.setPixelSize(16)
        self.base8Font = QFont('MS Shell Dlg 2', 8)
        self.base8Font.setPixelSize(11)
        self.setFont(self.base8Font)
        self.setWindowTitle('Configurator')
        icon = QIcon('Settings/icon.png')
        self.setWindowIcon(icon)
        self.setFixedSize(400, 100)
        self.show()
        '''if dM:
            self.setStyleSheet(open('Settings/darkModeSS').read())
            self.setStyle(QStyleFactory.create('Fusion'))
        else:
            self.setStyle(QStyleFactory().create('Fusion'))
            self.setStyleSheet('{background-color: #f0f0ed;} QAbstractItemView {border: 2px solid darkgray;selection-background-color: lightgray;}')'''
        self.initUI()

    def initUI(self):
        if self.judType == 'beforeCutAngleJudgments':
            self.maxVal = 70
        elif self.judType == 'accuracyJudgments':
            self.maxVal = 15
        elif self.judType == 'afterCutAngleJudgments':
            self.maxVal = 30
        elif self.judType == 'timeDependencyJudgments':
            self.maxVal = 1
        else:
            self.maxVal = None

        self.thrLabel = QLabel(f'Threshold (negative for else)', self)
        self.thrLabel.move(10, 10)
        self.thrLabel.resize(210, 20)
        self.thrLabel.setFont(self.arial12)
        self.thrLabel.show()

        if self.judType == 'timeDependencyJudgments':
            self.thrSB = QDoubleSpinBox(self)
            self.thrSB.setSingleStep(0.1)
            self.thrSB.setDecimals(3)
        else:
            self.thrSB = QSpinBox(self)
        if 'threshold' in self.jud:
            self.thrSB.setValue(self.jud['threshold'])
        else:
            self.thrSB.setValue(-1)
        self.thrSB.move(230, 10)
        self.thrSB.resize(160, 23)
        self.thrSB.setMinimum(-1)
        self.thrSB.setMaximum(self.maxVal)
        self.thrSB.show()

        self.textLabel = QLabel('Text', self)
        self.textLabel.move(10, 40)
        self.textLabel.resize(30, 20)
        self.textLabel.setFont(self.arial12)
        self.textLabel.show()

        self.textTB = QLineEdit(self.jud['text'], self)
        self.textTB.move(50, 40)
        self.textTB.resize(340, 23)
        self.textTB.show()

        self.confirmButton = QPushButton('Confirm', self)
        self.confirmButton.move(10, 70)
        self.confirmButton.resize(380, 23)
        self.confirmButton.clicked.connect(self.confirmClick)
        self.confirmButton.show()

    def confirmClick(self):
        if self.thrSB.value() < 0:
            if 'threshold' in self.jud:
                self.jud.pop('threshold')
        else:
            self.jud['threshold'] = self.thrSB.value()
            self.jud['text'] = self.textTB.text()
            self.conf[self.judType][self.ind] = self.jud
            self.hide()

    def closeEvent(self, event):
        if self.new:
            self.conf['judgments'].pop(-1)

    def get_conf(self):
        return self.conf
