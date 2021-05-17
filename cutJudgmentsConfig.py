from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QStyleFactory
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
        self.setFixedSize(400, 130)
        self.show()
        if dM:
            self.setStyleSheet(open('Settings/darkModeSS').read())
            self.setStyle(QStyleFactory.create('Windows'))
        else:
            self.setStyle(QStyleFactory().create('Fusion'))
            self.setStyleSheet('{background-color: #f0f0ed;} QAbstractItemView {border: 2px solid darkgray;selection-background-color: lightgray;}')
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

        self.thrLabel = QLabel(f'Threshold (between 0 and {self.maxVal})', self)
        self.thrLabel.move(10, 10)
        self.thrLabel.resize(210, 20)
        self.thrLabel.setFont(self.arial12)
        self.thrLabel.show()

        self.thrTB = QLineEdit(self)
        if 'threshold' in self.jud:
            self.thrTB.setText(str(self.jud['threshold']))
        self.thrTB.move(230, 10)
        self.thrTB.resize(160, 23)
        self.thrTB.show()

        self.thrWarningLabel = QLabel(self)
        self.thrWarningLabel.move(10, 40)
        self.thrWarningLabel.resize(380, 20)
        self.thrWarningLabel.setFont(self.arial12Bold)
        self.thrWarningLabel.setAlignment(Qt.AlignCenter)
        self.thrWarningLabel.show()

        self.textLabel = QLabel('Text', self)
        self.textLabel.move(10, 70)
        self.textLabel.resize(30, 20)
        self.textLabel.setFont(self.arial12)
        self.textLabel.show()

        self.textTB = QLineEdit(self.jud['text'], self)
        self.textTB.move(50, 70)
        self.textTB.resize(340, 23)
        self.textTB.show()

        self.confirmButton = QPushButton('Confirm', self)
        self.confirmButton.move(10, 100)
        self.confirmButton.resize(380, 23)
        self.confirmButton.clicked.connect(self.confirmClick)
        self.confirmButton.show()

    def confirmClick(self):
        isDataCorrect = self.checkData()
        if isDataCorrect:
            if self.thrTB.text() == '':
                if 'threshold' in self.jud:
                    self.jud.pop('threshold')
            else:
                if self.judType == 'timeDependencyJudgments':
                    self.jud['threshold'] = float(self.thrTB.text().replace(',', '.'))
                else:
                    self.jud['threshold'] = int(self.thrTB.text())

            self.jud['text'] = self.textTB.text()
            self.conf[self.judType][self.ind] = self.jud
            self.hide()

    def closeEvent(self, event):
        if self.new:
            self.conf['judgments'].pop(-1)

    def checkData(self):
        if self.thrTB.text() == '':
            return True

        if self.judType == 'timeDependencyJudgments':
            thr = self.thrTB.text().replace(',', '.')
            try:
                num = float(thr)
            except ValueError:
                self.thrWarningLabel.setText(f'{thr} is not a valid number')
                return False

            if num > 1:
                self.thrWarningLabel.setText(f'{num} is greater than 1')
                return False

            elif num < 0:
                self.thrWarningLabel.setText(f'{num} is lower than 0')
                return False

            else:
                return True

        else:
            try:
                num = int(self.thrTB.text())
            except ValueError:
                self.thrWarningLabel.setText(f'{self.thrTB.text()} is not a valid number')
                return False

            if num > self.maxVal:
                self.thrWarningLabel.setText(f'{num} is greater than {self.maxVal}')
                return False
            elif num < 0:
                self.thrWarningLabel.setText(f'{num} is lower than 0')
                return False
            else:
                return True

    def get_conf(self):
        return self.conf
