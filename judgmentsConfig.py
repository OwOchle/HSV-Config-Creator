from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QColorDialog, QSlider, QCheckBox, QStyleFactory
from PyQt5.QtWidgets import QSpinBox, QDoubleSpinBox
from PyQt5.QtGui import QFont, QIcon, QColor, QPainter, QBrush
from PyQt5.QtCore import Qt
from formattableCharacterWindow import addToken


class judgmentsConfig(QWidget):

    def __init__(self, threshold_ind, conf, dM, new=False):
        super().__init__()
        self.new = new
        self.setWindowTitle('Configurator')
        self.setFixedSize(400, 220)
        self.thr_ind = threshold_ind
        self.conf = conf
        self.jud = self.conf['judgments'][self.thr_ind]
        self.arial12Bold = QFont('Arial', 12)
        self.arial12 = QFont('Arial', 12)
        self.arial12.setPixelSize(16)
        self.base8Font = QFont('MS Shell Dlg 2', 8)
        self.base8Font.setPixelSize(11)
        self.setFont(self.base8Font)
        icon = QIcon('Settings/icon.png')
        self.setWindowIcon(icon)
        self.dM = dM
        '''if dM:
            self.setStyleSheet(open('Settings/darkModeSS').read())
            self.setStyle(QStyleFactory.create('Fusion'))
        else:
            self.setStyle(QStyleFactory().create('Fusion'))
            self.setStyleSheet('{background-color: #f0f0ed;} QAbstractItemView {border: 2px solid darkgray;selection-background-color: lightgray;}')'''
        self.initUI()
        self.show()

    def initUI(self):
        self.threLabel = QLabel('Threshold (negative for else)', self)
        self.threLabel.setFont(self.arial12)
        self.threLabel.move(10, 10)
        self.threLabel.resize(280, 20)
        self.threLabel.show()

        self.threSB = QSpinBox(self)
        self.threSB.setMinimum(-1)
        self.threSB.setMaximum(115)
        if 'threshold' not in self.jud:
            self.threSB.setValue(-1)
        else:
            self.threSB.setValue(self.jud['threshold'])
        self.threSB.move(220, 10)
        self.threSB.resize(50, 23)
        self.threSB.show()

        self.colorButton = QPushButton('Click here to choose a color', self)
        self.colorButton.move(10, 40)
        self.colorButton.resize(150, 23)
        self.colorButton.clicked.connect(self.colorButtonClick)
        self.colorButton.show()

        self.confirmButton = QPushButton('Confirm', self)
        self.confirmButton.move(10, 190)
        self.confirmButton.resize(380, 23)
        self.confirmButton.clicked.connect(self.confirmButtonClick)
        self.confirmButton.show()

        self.glowLabel = QLabel('Glow (between 0 and 1)', self)
        self.glowLabel.move(10, 70)
        self.glowLabel.resize(170, 20)
        self.glowLabel.setFont(self.arial12)
        self.glowLabel.show()

        self.glowSlider = QSlider(Qt.Horizontal, self)
        self.glowSlider.setValue(round(self.jud['color'][3], 2) * 100)
        self.glowSlider.setSingleStep(1)
        self.glowSlider.setMaximum(100)
        self.glowSlider.setMinimum(0)
        self.glowSlider.resize(150, 23)
        self.glowSlider.move(180, 70)
        self.glowSlider.valueChanged.connect(self.glowSliderVChanged)
        self.glowSlider.show()

        self.glowSB = QDoubleSpinBox(self)
        self.glowSB.setMaximum(1)
        self.glowSB.setDecimals(2)
        self.glowSB.setSingleStep(0.1)
        self.glowSB.setValue(self.jud['color'][3])
        self.glowSB.move(340, 70)
        self.glowSB.resize(50, 23)
        self.glowSB.valueChanged.connect(self.glowSBChanged)
        self.glowSB.show()

        self.cColor = QColor(int(self.jud['color'][0] * 255), int(self.jud['color'][1] * 255),
                        int(self.jud['color'][2] * 255), 255)
        self.colorChoose = QColorDialog(self)
        self.colorChoose.setCurrentColor(self.cColor)
        self.colorChoose.colorSelected.connect(self.colorChanged)
        self.colorChoose.hide()

        self.fadeCB = QCheckBox('Fade', self)
        self.fadeCB.setFont(self.arial12)
        self.fadeCB.move(10, 100)
        self.fadeCB.resize(70, 23)

        if 'fade' in self.jud:
            if self.jud['fade']:
                self.fadeCB.setChecked(True)
        self.fadeCB.show()

        if self.conf['displayMode'] == 'numeric':
            return

        self.textLabel = QLabel('Text', self)
        self.textLabel.setFont(self.arial12)
        self.textLabel.move(10, 130)
        self.textLabel.resize(30, 20)
        self.textLabel.show()

        self.textTB = QLineEdit(self.jud['text'], self)
        self.textTB.move(50, 130)
        self.textTB.resize(340, 23)
        self.textTB.show()

        if self.conf['displayMode'] == 'format':
            self.addFDButton = QPushButton("Add formatting token", self)
            self.addFDButton.move(10, 160)
            self.addFDButton.resize(120, 23)
            self.addFDButton.clicked.connect(self.addTokenClick)
            self.addFDButton.show()

    def colorChanged(self):
        self.cColor = self.colorChoose.currentColor()
        self.update()

    def paintEvent(self, event):
        colorRec = QPainter()
        colorRec.begin(self)
        colorRec.setPen(self.cColor)
        colorRec.fillRect(170, 39, 220, 23, QBrush(self.cColor, Qt.SolidPattern))
        colorRec.end()
    
    def addTokenClick(self):
        self.addTokenWin = addToken(self.dM)
        self.addTokenWin.confButton.clicked.connect(self.addTokenButtonClick)

    def addTokenButtonClick(self):
        nTXT = self.textTB.text() + self.addTokenWin.tokComB.currentText()
        self.addTokenWin.close()
        self.textTB.setText(nTXT)

    def glowSliderVChanged(self):
        rValue = round(self.glowSlider.value() / 100, 2)
        self.glowSB.setValue(rValue)

    def glowSBChanged(self):
        vRound = int(self.glowSB.value() * 100)
        self.glowSlider.setValue(vRound)

    def colorButtonClick(self):
        self.colorChoose.show()

    def confirmButtonClick(self):
        if self.threSB.value() < 0:
            if 'threshold' in self.jud:
                self.jud.pop('threshold')
        else:
            self.jud['threshold'] = self.threSB.value()

        self.hide()
        col = self.colorChoose.currentColor().getRgb()
        col = [round(col[0] / 255, 2), round(col[1] / 255, 2), round(col[2] / 255, 2),
               self.glowSB.value()]
        self.jud['color'] = col
        self.jud['fade'] = self.fadeCB.isChecked()
        self.jud['text'] = self.textTB.text()
        self.conf['judgments'][self.thr_ind] = self.jud

    def closeEvent(self, event):
        if self.new:
            self.conf['judgments'].pop(-1)

    def get_conf(self):
        return self.conf
