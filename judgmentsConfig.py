from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QColorDialog, QSlider, QCheckBox, QStyleFactory
from PyQt5.QtGui import QFont, QIcon, QColor, QPainter, QBrush
from PyQt5.QtCore import Qt
from formattableCharacterWindow import addToken


class judgmentsConfig(QWidget):

    def __init__(self, threshold_ind, conf, dM, new=False):
        super().__init__()
        self.new = new
        self.setWindowTitle('Configurator')
        self.setFixedSize(400, 300)
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
        if dM:
            self.setStyleSheet(open('Settings/darkModeSS').read())
            self.setStyle(QStyleFactory.create('Windows'))
        else:
            self.setStyle(QStyleFactory().create('Fusion'))
            self.setStyleSheet('{background-color: #f0f0ed;} QAbstractItemView {border: 2px solid darkgray;selection-background-color: lightgray;}')
        self.initUI()
        self.show()

    def initUI(self):
        self.threLabel = QLabel('Threshold (between 0 and 115 or empty)', self)
        self.threLabel.setFont(self.arial12)
        self.threLabel.move(10, 10)
        self.threLabel.resize(280, 20)
        self.threLabel.show()

        self.threLabelError = QLabel(self)
        self.threLabelError.setAlignment(Qt.AlignCenter)
        self.threLabelError.setFont(self.arial12Bold)
        self.threLabelError.resize(380, 20)
        self.threLabelError.move(10, 30)

        if 'threshold' not in self.jud:
            self.threTB = QLineEdit(self)
        else:
            self.threTB = QLineEdit(str(self.jud['threshold']), self)
        self.threTB.move(300, 10)
        self.threTB.resize(50, 23)
        self.threTB.show()

        self.colorButton = QPushButton('Click here to choose a color', self)
        self.colorButton.move(10, 60)
        self.colorButton.resize(150, 23)
        self.colorButton.clicked.connect(self.colorButtonClick)
        self.colorButton.show()

        self.confirmButton = QPushButton('Confirm', self)
        self.confirmButton.move(10, 270)
        self.confirmButton.resize(380, 23)
        self.confirmButton.clicked.connect(self.confirmButtonClick)
        self.confirmButton.show()

        self.glowLabel = QLabel('Glow (between 0 and 1)', self)
        self.glowLabel.move(10, 90)
        self.glowLabel.resize(170, 20)
        self.glowLabel.setFont(self.arial12)
        self.glowLabel.show()

        self.glowSlider = QSlider(Qt.Horizontal, self)
        self.glowSlider.setValue(round(self.jud['color'][3], 2) * 100)
        self.glowSlider.setSingleStep(1)
        self.glowSlider.setMaximum(100)
        self.glowSlider.setMinimum(0)
        self.glowSlider.resize(150, 23)
        self.glowSlider.move(180, 90)
        self.glowSlider.valueChanged.connect(self.glowSliderVChanged)
        self.glowSlider.show()

        self.glowTB = QLineEdit(str(round(self.jud['color'][3], 2)), self)
        self.glowTB.move(340, 90)
        self.glowTB.resize(50, 23)
        self.glowTB.textChanged.connect(self.glowTBTChanged)
        self.glowTB.show()

        self.cColor = QColor(int(self.jud['color'][0] * 255), int(self.jud['color'][1] * 255),
                        int(self.jud['color'][2] * 255), 255)
        self.colorChoose = QColorDialog(self)
        self.colorChoose.setCurrentColor(self.cColor)
        self.colorChoose.colorSelected.connect(self.colorChanged)
        self.colorChoose.hide()

        self.fadeCB = QCheckBox('Fade', self)
        self.fadeCB.setFont(self.arial12)
        self.fadeCB.move(10, 120)
        self.fadeCB.resize(70, 23)

        if 'fade' in self.jud:
            if self.jud['fade']:
                self.fadeCB.setChecked(True)
        self.fadeCB.show()

        if self.conf['displayMode'] == 'numeric':
            return

        self.textLabel = QLabel('Text', self)
        self.textLabel.setFont(self.arial12)
        self.textLabel.move(10, 150)
        self.textLabel.resize(30, 20)
        self.textLabel.show()

        self.textTB = QLineEdit(self.jud['text'], self)
        self.textTB.move(50, 150)
        self.textTB.resize(340, 23)
        self.textTB.show()

        if self.conf['displayMode'] == 'format':
            self.addFDButton = QPushButton("Add formatting token", self)
            self.addFDButton.move(10, 180)
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
        colorRec.fillRect(170, 60, 220, 23, QBrush(self.cColor, Qt.SolidPattern))
        colorRec.end()
    
    def addTokenClick(self):
        self.addTokenWin = addToken(self.dM)
        self.addTokenWin.confButton.clicked.connect(self.addTokenButtonClick)

    def addTokenButtonClick(self):
        ntxt = self.textTB.text() + self.addTokenWin.tokComB.currentText()
        self.addTokenWin.close()
        self.textTB.setText(ntxt)

    def glowSliderVChanged(self):
        rvalue = round(self.glowSlider.value() / 100, 2)
        self.glowTB.setText(str(rvalue))

    def glowTBTChanged(self):
        try:
            float(self.glowTB.text())
        except ValueError:
            return
        else:
            vround = int(round(float(self.glowTB.text()), 2) * 100)
            self.glowSlider.setValue(vround)

    def colorButtonClick(self):
        self.colorChoose.show()

    def confirmButtonClick(self):
        isDataCorrect = self.checkData()
        if isDataCorrect:
            if self.threTB.text() == '':
                if 'threshold' in self.jud:
                    self.jud.pop('threshold')
            else:
                self.jud['threshold'] = int(self.threTB.text())

            self.hide()
            col = self.colorChoose.currentColor().getRgb()
            col = [round(col[0] / 255, 2), round(col[1] / 255, 2), round(col[2] / 255, 2), round(float(self.glowSlider.value() / 100), 2)]
            self.jud['color'] = col
            self.jud['fade'] = self.fadeCB.isChecked()
            self.jud['text'] = self.textTB.text()
            self.conf['judgments'][self.thr_ind] = self.jud

    def checkData(self):
        if self.threTB.text() == '':
            return True
        else:
            try:
                num = int(self.threTB.text())
            except ValueError:
                self.threLabelError.setText(self.threTB.text() + ' is not a valid number')
                self.threLabelError.show()
                return False

            if num > 115:
                self.threLabelError.setText(self.threTB.text() + ' is greater than 115')
                return False
            elif num < 0:
                self.threLabelError.setText(self.threTB.text() + ' is lower than 0')
                return False
            else:
                return True

    def closeEvent(self, event):
        if self.new:
            self.conf['judgments'].pop(-1)

    def get_conf(self):
        return self.conf
