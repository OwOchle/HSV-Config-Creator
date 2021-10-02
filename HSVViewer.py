from PyQt5.QtWidgets import QWidget, QSlider, QSpinBox, QDoubleSpinBox, QLabel, QApplication
from PyQt5.QtGui import QFont, QPainter, QColor, QBrush, QFontDatabase, QIcon
from PyQt5.QtCore import Qt
import sys
import json
import traceback
from usefulFunctions import threSort, RGBA2RGB, getJudFromScore
import re


class Viewer(QWidget):

    def __init__(self, *, confPath=None, conf=None):
        super().__init__()
        if not confPath and not conf:
            try:
                self.conf = json.loads(open(sys.argv[1]).read())
            except IndexError:
                sys.exit(1)
        else:
            if conf:
                self.conf = conf
            else:
                self.conf = json.loads(open(confPath).read())
        self.setBaseSize(800, 500)
        self.setWindowTitle('HSV Simulator')
        self.baseFont = QFont('Arial', 12)
        familyID = QFontDatabase.addApplicationFont('Settings/Teko-Medium.ttf')
        fontName = QFontDatabase.applicationFontFamilies(familyID)[0]
        self.tekoFont = QFont(fontName)
        self.tekoFont.setPixelSize(50)
        self.setWindowIcon(QIcon('Settings/icon.png'))
        self.drawUI()
        self.show()

    def drawUI(self):
        self.BCLabel = QLabel('Before cut angle', self)
        self.BCLabel.setFont(self.baseFont)
        self.BCLabel.setGeometry(10, 10, 230, 20)
        self.BCLabel.setAlignment(Qt.AlignCenter)
        self.BCLabel.show()

        self.BCSlider = QSlider(self)
        self.BCSlider.setOrientation(Qt.Horizontal)
        self.BCSlider.setGeometry(10, 40, 160, 23)
        self.BCSlider.setRange(0, 70)
        self.BCSlider.valueChanged.connect(lambda x: self.BCSB.setValue(x))
        self.BCSlider.valueChanged.connect(self.updateAll)
        self.BCSlider.show()

        self.BCSB = QSpinBox(self)
        self.BCSB.setGeometry(180, 40, 60, 23)
        self.BCSB.setValue(self.BCSlider.value())
        self.BCSB.setRange(0, 70)
        self.BCSB.valueChanged.connect(lambda x: self.BCSlider.setValue(x))
        self.BCSB.valueChanged.connect(self.updateAll)
        self.BCSB.show()

        self.AccLabel = QLabel('Accuracy', self)
        self.AccLabel.setFont(self.baseFont)
        self.AccLabel.setGeometry(10, 70, 230, 20)
        self.AccLabel.setAlignment(Qt.AlignCenter)
        self.AccLabel.show()

        self.AccSlider = QSlider(self)
        self.AccSlider.setOrientation(Qt.Horizontal)
        self.AccSlider.setGeometry(10, 100, 160, 23)
        self.AccSlider.setRange(0, 15)
        self.AccSlider.valueChanged.connect(lambda x: self.AccSB.setValue(x))
        self.AccSlider.valueChanged.connect(self.updateAll)
        self.AccSlider.show()

        self.AccSB = QSpinBox(self)
        self.AccSB.setGeometry(180, 100, 60, 23)
        self.AccSB.setValue(self.AccSlider.value())
        self.AccSB.setRange(0, 15)
        self.AccSB.valueChanged.connect(lambda x: self.AccSlider.setValue(x))
        self.AccSB.valueChanged.connect(self.updateAll)
        self.AccSB.show()

        self.ACLabel = QLabel('After cut angle', self)
        self.ACLabel.setFont(self.baseFont)
        self.ACLabel.setGeometry(10, 130, 230, 20)
        self.ACLabel.setAlignment(Qt.AlignCenter)
        self.ACLabel.show()

        self.ACSlider = QSlider(self)
        self.ACSlider.setOrientation(Qt.Horizontal)
        self.ACSlider.setGeometry(10, 160, 160, 23)
        self.ACSlider.setRange(0, 30)
        self.ACSlider.valueChanged.connect(lambda x: self.ACSB.setValue(x))
        self.ACSlider.valueChanged.connect(self.updateAll)
        self.ACSlider.show()

        self.ACSB = QSpinBox(self)
        self.ACSB.setGeometry(180, 160, 60, 23)
        self.ACSB.setValue(self.ACSlider.value())
        self.ACSB.setRange(0, 30)
        self.ACSB.valueChanged.connect(lambda x: self.ACSlider.setValue(x))
        self.ACSB.valueChanged.connect(self.updateAll)
        self.ACSB.show()

        self.tDLabel = QLabel('Time dependency', self)
        self.tDLabel.setFont(self.baseFont)
        self.tDLabel.setGeometry(10, 190, 230, 20)
        self.tDLabel.setAlignment(Qt.AlignCenter)
        self.tDLabel.show()

        self.tDSlider = QSlider(self)
        self.tDSlider.setOrientation(Qt.Horizontal)
        self.tDSlider.setGeometry(10, 220, 160, 23)
        self.tDSlider.setRange(0, 100)
        self.tDSlider.valueChanged.connect(self.updateAll)
        self.tDSlider.setSingleStep(10)
        self.tDSlider.valueChanged.connect(lambda x: self.tDSB.setValue(round(x / 100, 2)))
        self.tDSlider.show()

        self.tDSB = QDoubleSpinBox(self)
        self.tDSB.setGeometry(180, 220, 60, 23)
        self.tDSB.setValue(self.tDSlider.value() / 100)
        self.tDSB.setDecimals(2)
        self.tDSB.setRange(0, 1)
        self.tDSB.setSingleStep(0.1)
        self.tDSB.valueChanged.connect(lambda x: self.tDSlider.setValue(int(x * 100)))
        self.tDSB.valueChanged.connect(self.updateAll)
        self.tDSB.show()

        self.drawnLabel = QLabel(self)
        self.drawnLabel.setGeometry(250, 10, 340, 340)
        self.drawnLabel.setAlignment(Qt.AlignCenter)
        self.drawnLabel.setFont(self.tekoFont)
        self.drawnLabel.setText(str(self.BCSB.value()))
        self.drawnLabel.setStyleSheet('color: #ffffff')
        self.show()

        self.updateAll()

    def updateFromMainWindow(self, newConf):
        self.conf = newConf
        self.updateAll()

    def updateAll(self):
        self.drawnLabel.setStyleSheet(f'color: {self.getColorFromScore()}')
        score = self.BCSB.value() + self.ACSB.value() + self.AccSB.value()
        if self.conf['displayMode'] == 'format':
            cDict = getJudFromScore(self.conf['judgments'], score)
            formatText = re.sub('<[^>]+>', '', cDict['text'])
            formatText = formatText.replace('%n', '\n').replace('%%', '%').replace('%s', str(score))
            formatText = formatText.replace('%b', str(self.BCSB.value())).replace('%a', str(self.ACSB.value()))
            formatText = formatText.replace('%c', str(self.AccSB.value())).replace('%t', str(self.tDSB.value()))
            if '%B' in formatText or '%A' in formatText or '%C' in formatText:
                BToken = getJudFromScore(self.conf['beforeCutAngleJudgments'], self.BCSB.value())['text']
                CToken = getJudFromScore(self.conf['accuracyJudgments'], self.AccSB.value())['text']
                AToken = getJudFromScore(self.conf['afterCutAngleJudgments'], self.ACSB.value())['text']
                formatText = formatText.replace('%B', BToken).replace('%C', CToken).replace('%A', AToken)
            if '%T' in formatText and self.conf['timeDependencyJudgments']:
                TToken = getJudFromScore(self.conf['timeDependencyJudgments'], self.tDSB.value())['text']
                formatText = formatText.replace('%T', TToken)

            self.drawnLabel.setText(formatText)

        elif self.conf['displayMode'] == 'numeric':
            self.drawnLabel.setText(str(score))

        elif self.conf['displayMode'] == 'textOnly':
            cDict = getJudFromScore(self.conf['judgments'], score)
            formatText = re.sub('<[^>]+>', '', cDict['text'])
            self.drawnLabel.setText(formatText)

        elif self.conf['displayMode'] == 'scoreOnTop':
            cDict = getJudFromScore(self.conf['judgments'], score)
            formatText = re.sub('<[^>]+>', '', cDict['text'])
            self.drawnLabel.setText(str(score) + '\n' + formatText)

        else:
            cDict = getJudFromScore(self.conf['judgments'], score)
            formatText = re.sub('<[^>]+>', '', cDict['text'])
            self.drawnLabel.setText(formatText + '\n' + str(score))

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        color = QColor.fromRgb(0, 0, 0, 255)
        painter.setPen(color)
        painter.fillRect(250, 10, self.width() - 260, self.height() - 20, QBrush(color, Qt.SolidPattern))
        painter.end()

    def resizeEvent(self, event):
        self.drawnLabel.setGeometry(250, 10, self.width() - 260, self.height() - 20)
        self.paintEvent(None)

    def getColorFromScore(self):
        score = self.BCSB.value() + self.ACSB.value() + self.AccSB.value()
        judgmentsList = threSort(self.conf['judgments'])
        jud = getJudFromScore(judgmentsList, score)
        fgColor = (int(jud["color"][0] * 255), int(jud["color"][1] * 255), int(jud["color"][2] * 255),
                   jud['color'][3])
        alphedColor = RGBA2RGB(fgColor, (0, 0, 0))
        color = '#%02x%02x%02x' % alphedColor
        return color


sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback_e):
    sys.__excepthook__(exctype, value, traceback_e)
    with open('Settings/Logs/crash-report.log', 'a+') as cr:
        traceback.print_exception(exctype, value, traceback_e, file=cr)
    sys.exit(1)


sys.excepthook = my_exception_hook


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Viewer()
    sys.exit(app.exec())
