import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QLabel, QLineEdit, QCheckBox, QComboBox
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QFileDialog, QStyleFactory
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
import os
import json
import webbrowser
from judgmentsConfig import judgmentsConfig
from sorter import threSort
from newConfigWindow import newConf
from cutJudgmentsConfig import cutJudgmentsConfig
from duplicationWindow import duplWin
from shutil import copyfile
import traceback


with open('Settings/settings.json') as f:
    settings = json.loads(f.read())
if settings['beatSaberPath'] and os.path.exists(settings['beatSaberPath']):
    path = settings['beatSaberPath']
    dark_mode = settings['darkMode']
    isFirstTimeOpening = False
else:
    path = ''
    dark_mode = settings['darkMode']
    isFirstTimeOpening = True


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 600
        self.windowName = 'HSV Configurator (Version : 0.1.8)'
        self.Arial12Font = QFont('Arial', 12)
        self.Arial12Font.setBold(True)
        self.Arial12Font.setPixelSize(16)
        self.Arial12FontNB = QFont('Arial', 12)
        self.Arial12FontNB.setPixelSize(16)
        self.base12Font = QFont('MS Shell Dlg 2', 12)
        self.base12Font.setPixelSize(16)
        self.base8Font = QFont('MS Shell Dlg 2', 8)
        self.base8Font.setPixelSize(11)
        self.setFont(self.base8Font)
        self.al = Qt.AlignCenter
        self.initUI()
        self.darkMode()

    def initUI(self):
        self.setMenuButton()
        self.menuButton.hide()
        self.setBackButton()
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.fbDialog = QFileDialog(self)
        self.fbDialog.setStyle(QStyleFactory.create('fusion'))
        self.fbDialog.setFileMode(QFileDialog.Directory)
        self.fbDialog.setDirectory(path)
        self.setWindowIcon(QIcon('Settings/icon.png'))
        self.show()
        if isFirstTimeOpening:
            self.settingsScene()
        else:
            self.menuScene()

    def setMenuButton(self):
        self.menuButton = QPushButton('Menu (without saving)', self)
        self.menuButton.move(670, 10)
        self.menuButton.resize(120, 23)
        self.menuButton.clicked.connect(self.backToMenuButtonClick)

    def setBackButton(self):
        self.backButton = QPushButton('Back', self)
        self.backButton.move(10, 570)
        self.backButton.resize(80, 23)
        self.backButton.clicked.connect(self.backToMenuButtonClick)
        self.show()

    def menuScene(self):
        self.setConfList()
        self.setWindowTitle(self.windowName)

        self.editButton = QPushButton('Edit', self)
        self.editButton.move(10, 570)
        self.editButton.resize(80, 23)
        self.editButton.clicked.connect(self.editClick)
        self.editButton.show()

        self.deleteButton = QPushButton('Delete', self)
        self.deleteButton.move(100, 570)
        self.deleteButton.resize(80, 23)
        self.deleteButton.clicked.connect(self.deleteClick)
        self.deleteButton.show()

        self.settingsButton = QPushButton('Settings', self)
        self.settingsButton.move(190, 570)
        self.settingsButton.resize(80, 23)
        self.settingsButton.clicked.connect(self.settingsClick)
        self.settingsButton.show()

        self.refreshButton = QPushButton('Refresh', self)
        self.refreshButton.move(280, 570)
        self.refreshButton.resize(80, 23)
        self.refreshButton.clicked.connect(self.refreshClick)
        self.refreshButton.show()

        self.newButton = QPushButton('New', self)
        self.newButton.move(370, 570)
        self.newButton.resize(80, 23)
        self.newButton.clicked.connect(self.newClick)
        self.newButton.show()

        self.plsSelConfLabel = QLabel('Please select a config', self)
        self.plsSelConfLabel.move(10, 540)
        self.plsSelConfLabel.setAlignment(self.al)
        self.plsSelConfLabel.resize(780, 30)
        self.plsSelConfLabel.setFont(self.Arial12Font)
        self.plsSelConfLabel.show()

        self.dupliButton = QPushButton('Copy', self)
        self.dupliButton.move(460, 570)
        self.dupliButton.resize(80, 23)
        self.dupliButton.clicked.connect(self.dupliClick)
        self.dupliButton.show()

        self.exitButton = QPushButton('Exit', self)
        self.exitButton.move(710, 570)
        self.exitButton.resize(80, 23)
        self.exitButton.clicked.connect(self.exitClick)
        self.exitButton.show()

    def dupliClick(self):
        if self.confList.currentItem():
            self.duplWin = duplWin(self.confList.currentItem().text(), dark_mode)
            self.duplWin.confirmButton.clicked.connect(self.duplWinClick)
        else:
            self.plsSelConfLabel.setText('You need to choose a config')

    def duplWinClick(self):
        name = self.duplWin.nameTB.text()
        name = name.replace('<', '_').replace('>', '_').replace(':', '_').replace('"', '_').replace('/', '_')
        name = name.replace('\\', '_').replace('|', '_').replace('?', '_').replace('*', '_')
        if name == '':
            self.duplWin.confirmLabel.setText('File name cannot be empty')
        else:
            if os.path.exists(path + self.duplWin.nameTB.text() + '.json'):
                self.duplWin.confirmLabel.setText('A config already exists with this name')
            else:
                self.duplWin.hide()
                src = path + self.confList.currentItem().data(Qt.UserRole)['path']
                dst = path + name + '.json'
                copyfile(src, dst)
        self.refreshClick()

    def exitClick(self):
        self.close()

    def setConfList(self):
        self.confList = QListWidget(self)
        self.confList.move(10, 10)
        self.confList.resize(780, 530)
        conf = os.listdir(path)
        for item in conf:
            if item[-5: len(item)] == '.json':
                Item = QListWidgetItem(item[0:-5])
                Item.setData(Qt.UserRole, {'path': item})
                Item.setFont(self.Arial12FontNB)
                self.confList.addItem(Item)
        self.confList.show()

    def newClick(self):
        self.newConfWin = newConf(dark_mode)
        self.newConfWin.confirmButton.clicked.connect(self.newConfWinClick)

    def newConfWinClick(self):
        name = self.newConfWin.nameTB.text()
        name = name.replace('<', '_').replace('>', '_').replace(':', '_').replace('"', '_').replace('/', '_')
        name = name.replace('\\', '_').replace('|', '_').replace('?', '_').replace('*', '_')
        self.newConfWin.close()

        with open('Settings/empty.json') as f2:
            with open(path + name + '.json', 'w') as f3:
                f3.write(f2.read())

        self.refreshClick()

    def deleteClick(self):
        if self.confList.currentItem():
            deleteWarning = QMessageBox(self)
            deleteWarning.setText('Are you sure you want to delete this config ?')
            deleteWarning.setWindowTitle('Deleting ' + self.confList.currentItem().text())
            deleteWarning.setIcon(QMessageBox.Warning)
            deleteWarning.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            deleteWarning.setDefaultButton(QMessageBox.Cancel)
            deleteWarning.buttonClicked.connect(lambda x: self.deleteConf(x))
            deleteWarning.show()
        else:
            self.plsSelConfLabel.setText('You need to choose a config')

    def deleteConf(self, button):
        if button.text() == 'OK':
            os.remove(path + self.confList.currentItem().text() + '.json')
            self.confList.takeItem(self.confList.currentRow())
        self.backToMenuButtonClick()

    def editClick(self):
        if self.confList.currentItem():
            self.hideAll()
            self.editScene1()
        else:
            self.plsSelConfLabel.setText('You need to choose a config')

    def hideAll(self):
        for item in self.children():
            item.hide()

    def settingsClick(self):
        self.hideAll()
        self.settingsScene()

    def settingsScene(self):
        self.bsPathLabel = QLabel('HitScoreVisualizer Configs Path', self)
        self.bsPathLabel.move(10, 0)
        self.bsPathLabel.resize(780, 30)
        self.bsPathLabel.setAlignment(self.al)
        self.bsPathLabel.setFont(self.base12Font)
        self.bsPathLabel.show()

        self.pathLabel = QLabel(path, self)
        self.pathLabel.move(10, 30)
        self.pathLabel.resize(700, 23)
        self.pathLabel.show()

        self.bsPathButton = QPushButton('Browse', self)
        self.bsPathButton.resize(70, 23)
        self.bsPathButton.move(720, 30)
        self.bsPathButton.clicked.connect(self.bsPathBrowseClick)
        self.bsPathButton.show()

        self.bsPathConfLabel = QLabel('Click "Back" button to save', self)
        self.bsPathConfLabel.setFont(self.Arial12Font)
        self.bsPathConfLabel.move(10, 53)
        self.bsPathConfLabel.resize(780, 30)
        self.bsPathConfLabel.setAlignment(self.al)
        self.bsPathConfLabel.show()

        self.darkModeCB = QCheckBox('Dark Mode', self)
        self.darkModeCB.move(10, 100)
        self.darkModeCB.setFont(self.Arial12FontNB)
        self.darkModeCB.resize(120, 23)
        if dark_mode:
            self.darkModeCB.setChecked(True)
        else:
            self.darkModeCB.setChecked(False)
        self.darkModeCB.stateChanged.connect(lambda: self.setDarkMode(self.darkModeCB.isChecked()))
        self.darkModeCB.show()

        self.backButton.show()

    def setDarkMode(self, mode):
        global dark_mode
        dark_mode = mode
        self.darkMode()

    def darkMode(self):
        global dark_mode
        if dark_mode:
            self.setStyle(QStyleFactory.create('Windows'))
            self.setStyleSheet(open('Settings/darkModeSS').read())
            self.fbDialog.setStyleSheet(
                'QLabel {color: #ffffff;} QWidget{background-color: #121212;} QLineEdit{color: #ffffff;} QComboBox{color: #ffffff;} QListView{color: #ffffff;}')
            self.base8Font.setPixelSize(11)
            self.menuButton.setFont(self.base8Font)
        else:
            self.setStyle(QStyleFactory().create('Fusion'))
            self.fbDialog.setStyleSheet('QWidget{background-color: #f0f0ed}')
            self.setStyleSheet('{background-color: #f0f0ed} QAbstractItemView {border: 2px solid darkgray;selection-background-color: lightgray;}')
        self.settingsUpdate()

    def bsPathBrowseClick(self):
        self.fbDialog.currentChanged.connect(lambda: self.pathLabel.setText(self.fbDialog.directory().path()))
        self.fbDialog.show()

    def backToMenuButtonClick(self):
        if self.fbDialog:
            self.setPath()
        self.hideAll()
        self.menuScene()

    def setPath(self):
        global path
        path = self.fbDialog.directory().path()
        if path[-1] != '/':
            path += '/'
        self.settingsUpdate()

    def settingsUpdate(self):
        settingsUpdate = {'beatSaberPath': path, 'darkMode': dark_mode}
        with open('Settings/settings.json', 'w') as f2:
            json.dump(settingsUpdate, f2)

    def editScene1(self):
        self.menuButton.show()
        self.setWindowTitle(f'{self.windowName} - Editing {self.confList.currentItem().text()}')

        with open(path + self.confList.currentItem().data(Qt.UserRole)["path"]) as f2:
            self.conf = json.loads(f2.read())
            self.conf['judgments'] = threSort(self.conf['judgments'])
        self.checkConfig()
        self.nextEdit1Button = QPushButton('Next', self)
        self.nextEdit1Button.move(710, 570)
        self.nextEdit1Button.resize(80, 23)
        self.nextEdit1Button.clicked.connect(self.edit1NextClick)
        self.nextEdit1Button.show()

        self.saveConfLabel = QLabel('Changes will be saved when clicking Next or Back button', self)
        self.saveConfLabel.setFont(self.Arial12Font)
        self.saveConfLabel.setAlignment(self.al)
        self.saveConfLabel.resize(620, 23)
        self.saveConfLabel.move(90, 570)
        self.saveConfLabel.show()

        self.nameLabel = QLabel('Config Name :', self)
        self.nameLabel.resize(105, 23)
        self.nameLabel.move(10, 10)
        self.nameLabel.setFont(self.base12Font)
        self.nameLabel.show()

        self.nameTB = QLabel(self.confList.currentItem().text(), self)
        self.nameTB.setFont(self.Arial12Font)
        self.nameTB.move(120, 10)
        self.nameTB.resize(550, 22)
        self.nameTB.show()

        self.isDefaultCB = QCheckBox('Is it the default config', self)
        self.isDefaultCB.setFont(self.base12Font)
        self.isDefaultCB.move(10, 50)
        self.isDefaultCB.resize(180, 23)
        if self.conf['isDefaultConfig']:
            self.isDefaultCB.setChecked(True)
        self.isDefaultCB.show()

        self.textModeLabel = QLabel('Text mode', self)
        self.textModeLabel.resize(80, 23)
        self.textModeLabel.move(10, 90)
        self.textModeLabel.setFont(self.base12Font)
        self.textModeLabel.show()

        self.textModeComB = QComboBox(self)
        self.textModeComB.addItem('Formatable')
        self.textModeComB.addItem('Only Score')
        self.textModeComB.addItem('Only Text')
        self.textModeComB.addItem('Score above text (non formatable)')
        self.textModeComB.addItem('Text above score (non formatable)')

        if self.conf['displayMode'] == 'format':
            self.textModeComB.setCurrentIndex(0)
        elif self.conf['displayMode'] == 'numeric':
            self.textModeComB.setCurrentIndex(1)
        elif self.conf['displayMode'] == 'textOnly':
            self.textModeComB.setCurrentIndex(2)
        elif self.conf['displayMode'] == 'scoreOnTop':
            self.textModeComB.setCurrentIndex(3)
        else:
            self.textModeComB.setCurrentIndex(4)

        self.textModeComB.resize(200, 23)
        self.textModeComB.move(90, 90)
        self.textModeComB.show()

        self.intermediateUpdateCB = QCheckBox('Do intermediate updates of the score', self)
        self.intermediateUpdateCB.setFont(self.base12Font)
        self.intermediateUpdateCB.move(10, 130)
        self.intermediateUpdateCB.resize(300, 23)
        if self.conf['doIntermediateUpdates']:
            self.intermediateUpdateCB.setChecked(True)
        self.intermediateUpdateCB.show()

        self.decimalTimeNumLabel = QLabel('Time dependency decimal precision (between 0 and 99)', self)
        self.decimalTimeNumLabel.move(10, 170)
        self.decimalTimeNumLabel.resize(400, 23)
        self.decimalTimeNumLabel.setFont(self.base12Font)
        self.decimalTimeNumLabel.show()

        self.decimalTimeNumTB = QLineEdit(str(self.conf['timeDependencyDecimalPrecision']), self)
        self.decimalTimeNumTB.move(420, 170)
        self.decimalTimeNumTB.resize(100, 23)
        self.decimalTimeNumTB.show()

        self.decimalTimeOffLabel = QLabel('Time dependency decimal offset (between 0 and 38)', self)
        self.decimalTimeOffLabel.move(10, 210)
        self.decimalTimeOffLabel.resize(400, 23)
        self.decimalTimeOffLabel.setFont(self.base12Font)
        self.decimalTimeOffLabel.show()

        self.decimalTimeOffTB = QLineEdit(str(self.conf['timeDependencyDecimalOffset']), self)
        self.decimalTimeOffTB.move(390, 210)
        self.decimalTimeOffTB.resize(100, 23)
        self.decimalTimeOffTB.show()

        self.fixedPosCB = QCheckBox('Is the score position static', self)
        self.fixedPosCB.setFont(self.base12Font)
        self.fixedPosCB.resize(210, 23)
        self.fixedPosCB.move(10, 250)
        if self.conf['useFixedPos']:
            self.fixedPosCB.setChecked(True)
            self.fixedPosCBChangeState(True)
        self.fixedPosCB.stateChanged.connect(self.fixedPosCBChangeState)
        self.fixedPosCB.show()

        self.edit1BackButton = QPushButton('Back', self)
        self.edit1BackButton.move(10, 570)
        self.edit1BackButton.resize(80, 23)
        self.edit1BackButton.clicked.connect(self.edit1BackClick)
        self.edit1BackButton.show()

        self.wikiButton = QPushButton('WIKI', self)
        self.wikiButton.setFont(self.Arial12Font)
        self.wikiButton.move(10, 530)
        self.wikiButton.resize(780, 30)
        self.wikiButton.show()
        self.wikiButton.clicked.connect(self.openWiki)

        self.edit1NSBackButton = QPushButton('Back (without saving)')

    def openWiki(self):
        webbrowser.open('https://github.com/ErisApps/HitScoreVisualizer#how-to-config-aka-config-explained')

    def checkConfig(self):
        conf = self.conf
        if 'isDefaultConfig' not in conf:
            self.conf['isDefaultConfig'] = False
        if 'useFixedPos' not in conf:
            self.conf['useFixedPos'] = False
        if 'doIntermediateUpdates' not in conf:
            self.conf['doIntermediateUpdates'] = False
        if 'timeDependencyDecimalPrecision' not in conf:
            self.conf['timeDependencyDecimalPrecision'] = 0
        if 'timeDependencyDecimalOffset' not in conf:
            self.conf['timeDependencyDecimalOffset'] = 0
        if 'fixedPosX' not in conf:
            self.conf['fixedPosX'] = 0.0
        if 'fixedPosY' not in conf:
            self.conf['fixedPosY'] = 0.0
        if 'fixedPosZ' not in conf:
            self.conf['fixedPosZ'] = 0.0
        if 'beforeCutAngleJudgments' not in conf:
            self.conf['beforeCutAngleJudgments'] = []
        if 'accuracyJudgments' not in conf:
            self.conf['accuracyJudgments'] = []
        if 'afterCutAngleJudgments' not in conf:
            self.conf['afterCutAngleJudgments'] = []
        if 'timeDependencyJudgments' not in conf:
            self.conf['timeDependencyJudgments'] = []

    def fixedPosCBChangeState(self, state):
        if state:
            self.posXLabel = QLabel('X', self)
            self.posXLabel.resize(10, 23)
            self.posXLabel.setFont(self.base12Font)
            self.posXLabel.move(240, 250)
            self.posXLabel.show()

            self.posXTB = QLineEdit(str(self.conf['fixedPosX']), self)
            self.posXTB.resize(100, 23)
            self.posXTB.move(260, 250)
            self.posXTB.show()

            self.posYLabel = QLabel('Y', self)
            self.posYLabel.resize(10, 23)
            self.posYLabel.setFont(self.base12Font)
            self.posYLabel.move(240, 280)
            self.posYLabel.show()

            self.posYTB = QLineEdit(str(self.conf['fixedPosY']), self)
            self.posYTB.resize(100, 23)
            self.posYTB.move(260, 280)
            self.posYTB.show()

            self.posZLabel = QLabel('Z', self)
            self.posZLabel.resize(10, 23)
            self.posZLabel.setFont(self.base12Font)
            self.posZLabel.move(240, 310)
            self.posZLabel.show()

            self.posZTB = QLineEdit(str(self.conf['fixedPosZ']), self)
            self.posZTB.resize(100, 23)
            self.posZTB.move(260, 310)
            self.posZTB.show()
        elif not state:
            self.posZTB.hide()
            self.posYTB.hide()
            self.posXTB.hide()

            self.posXLabel.hide()
            self.posYLabel.hide()
            self.posZLabel.hide()

    def saveToFile(self):
        with open(path + self.confList.currentItem().text() + '.json', 'w') as f2:
            json.dump(self.conf, f2)

    def edit1BackClick(self):
        self.conf['isDefaultConfig'] = self.isDefaultCB.isChecked()

        combSel = self.textModeComB.currentIndex()
        if combSel == 0:
            self.conf['displayMode'] = 'format'
        elif combSel == 1:
            self.conf['displayMode'] = 'numeric'
        elif combSel == 2:
            self.conf['displayMode'] = 'textOnly'
        elif combSel == 3:
            self.conf['displayMode'] = 'scoreOnTop'
        elif combSel == 4:
            self.conf['displayMode'] = ''

        self.conf['doIntermediateUpdates'] = self.intermediateUpdateCB.isChecked()
        try:
            int(self.decimalTimeNumTB.text())
        except TypeError:
            self.decimalTimeNumTB.setText('0')
        if int(self.decimalTimeNumTB.text()) > 99 or int(self.decimalTimeNumTB.text()) < 0:
            self.decimalTimeNumTB.setText('0')

        self.conf['timeDependencyDecimalPrecision'] = int(self.decimalTimeNumTB.text())

        try:
            int(self.decimalTimeOffTB.text())
        except TypeError:
            self.decimalTimeOffTB.setText('0')
        if int(self.decimalTimeOffTB.text()) > 38 or int(self.decimalTimeOffTB.text()) < 0:
            self.decimalTimeOffTB.setText('0')

        self.conf['timeDependencyDecimalOffset'] = int(self.decimalTimeOffTB.text())

        if self.fixedPosCB.isChecked():
            self.conf['useFixedPos'] = True
            try:
                float(self.posXTB.text())
            except TypeError:
                self.posXTB.setText('0.0')

            try:
                float(self.posYTB.text())
            except TypeError:
                self.posYTB.setText('0.0')

            try:
                float(self.posZTB.text())
            except TypeError:
                self.posZTB.setText('0.0')

            self.conf['fixedPosX'] = float(self.posXTB.text())
            self.conf['fixedPosY'] = float(self.posYTB.text())
            self.conf['fixedPosZ'] = float(self.posZTB.text())
        else:
            self.conf['useFixedPos'] = False
            self.conf['fixedPosX'] = 0.0
            self.conf['fixedPosY'] = 0.0
            self.conf['fixedPosZ'] = 0.0
        self.saveToFile()
        self.backToMenuButtonClick()

    def edit1NextClick(self):
        self.conf['isDefaultConfig'] = self.isDefaultCB.isChecked()

        combSel = self.textModeComB.currentIndex()
        if combSel == 0:
            self.conf['displayMode'] = 'format'
        elif combSel == 1:
            self.conf['displayMode'] = 'numeric'
        elif combSel == 2:
            self.conf['displayMode'] = 'textOnly'
        elif combSel == 3:
            self.conf['displayMode'] = 'scoreOnTop'
        elif combSel == 4:
            self.conf['displayMode'] = ''

        self.conf['doIntermediateUpdates'] = self.intermediateUpdateCB.isChecked()
        try:
            int(self.decimalTimeNumTB.text())
        except TypeError:
            self.decimalTimeNumTB.setText('0')
        if int(self.decimalTimeNumTB.text()) > 99 or int(self.decimalTimeNumTB.text()) < 0:
            self.decimalTimeNumTB.setText('0')

        self.conf['timeDependencyDecimalPrecision'] = int(self.decimalTimeNumTB.text())

        try:
            int(self.decimalTimeOffTB.text())
        except TypeError:
            self.decimalTimeOffTB.setText('0')
        if int(self.decimalTimeOffTB.text()) > 38 or int(self.decimalTimeOffTB.text()) < 0:
            self.decimalTimeOffTB.setText('0')

        self.conf['timeDependencyDecimalOffset'] = int(self.decimalTimeOffTB.text())

        if self.fixedPosCB.isChecked():
            self.conf['useFixedPos'] = True
            try:
                float(self.posXTB.text())
            except TypeError:
                self.posXTB.setText('0.0')

            try:
                float(self.posYTB.text())
            except TypeError:
                self.posYTB.setText('0.0')

            try:
                float(self.posZTB.text())
            except TypeError:
                self.posZTB.setText('0.0')

            self.conf['fixedPosX'] = float(self.posXTB.text())
            self.conf['fixedPosY'] = float(self.posYTB.text())
            self.conf['fixedPosZ'] = float(self.posZTB.text())
        else:
            self.conf['useFixedPos'] = False
            self.conf['fixedPosX'] = 0.0
            self.conf['fixedPosY'] = 0.0
            self.conf['fixedPosZ'] = 0.0

        self.saveToFile()
        self.hideAll()
        self.editScene2()

    def editScene2(self):
        self.menuButton.show()

        self.backEdit2Button = QPushButton('Back', self)
        self.backEdit2Button.move(10, 570)
        self.backEdit2Button.resize(80, 23)
        self.backEdit2Button.clicked.connect(self.edit2BackClick)
        self.backEdit2Button.show()

        self.nextEdit2Button = QPushButton('Next', self)
        self.nextEdit2Button.move(710, 570)
        self.nextEdit2Button.resize(80, 23)
        self.nextEdit2Button.clicked.connect(self.edit2NextClick)
        self.nextEdit2Button.show()
        self.saveConfLabel.show()

        self.thresholdList = QListWidget(self)
        self.listThre()
        self.thresholdList.move(10, 40)
        self.thresholdList.resize(640, 480)
        self.thresholdList.show()

        self.thresholdLabel = QLabel('Judgments List', self)
        self.thresholdLabel.move(10, 10)
        self.thresholdLabel.resize(640, 23)
        self.thresholdLabel.setAlignment(self.al)
        self.thresholdLabel.setFont(self.Arial12Font)
        self.thresholdLabel.show()

        self.newThrButton = QPushButton('New judgment', self)
        self.newThrButton.resize(130, 23)
        self.newThrButton.move(660, 40)
        self.newThrButton.clicked.connect(self.edit2NewThrClick)
        self.newThrButton.show()

        self.editThrButton = QPushButton('Edit judgment', self)
        self.editThrButton.move(660, 70)
        self.editThrButton.resize(130, 23)
        self.editThrButton.clicked.connect(self.edit2editThrClick)
        self.editThrButton.show()

        self.delThrButton = QPushButton('Delete judgment', self)
        self.delThrButton.resize(130, 23)
        self.delThrButton.move(660, 100)
        self.delThrButton.clicked.connect(self.edit2delThrClick)
        self.delThrButton.show()

        self.wikiButton.show()

    def listThre(self):
        self.thresholdList.clear()
        self.conf['judgments'] = threSort(self.conf['judgments'])
        for item in self.conf['judgments']:
            if 'threshold' not in item:
                qitem = QListWidgetItem('Else')
            else:
                qitem = QListWidgetItem(str(item['threshold']))
            qitem.setFont(self.Arial12FontNB)
            self.thresholdList.addItem(qitem)

    def edit2BackClick(self):
        self.saveToFile()
        self.hideAll()
        self.editScene1()

    def edit2NextClick(self):
        self.saveToFile()
        self.hideAll()
        self.editScene3()

    def edit2NewThrClick(self):
        self.conf['judgments'].append({'text': '', 'color': [0.0, 0.0, 0.0, 1.0]})
        self.threConfWin = judgmentsConfig(-1, self.conf, dark_mode, True)
        self.threConfWin.confirmButton.clicked.connect(self.edit2confirmEditClick)

    def edit2editThrClick(self):
        self.threConfWin = judgmentsConfig(self.thresholdList.currentIndex().row(), self.conf, dark_mode)
        self.threConfWin.confirmButton.clicked.connect(self.edit2confirmEditClick)

    def edit2confirmEditClick(self):
        dat = self.threConfWin.checkData()
        if dat:
            self.conf = self.threConfWin.get_conf()
            self.listThre()

    def editScene3(self):
        if 'timeDependencyJudgments' not in self.conf or self.conf['timeDependencyJudgments'] == None:
            self.conf['timeDependencyJudgments'] = []
        labSize = QSize(640, 20)
        listSize = QSize(640, 100)
        butSize = QSize(130, 23)

        self.menuButton.show()
        self.saveConfLabel.show()

        self.edit3BackButton = QPushButton('Back', self)
        self.edit3BackButton.move(self.backButton.pos())
        self.edit3BackButton.resize(self.backButton.size())
        self.edit3BackButton.clicked.connect(self.edit3BackClick)
        self.edit3BackButton.show()

        self.edit3NextButton = QPushButton('Next', self)
        self.edit3NextButton.move(self.nextEdit2Button.pos())
        self.edit3NextButton.resize(self.nextEdit2Button.size())
        self.edit3NextButton.clicked.connect(self.edit3NextClick)
        self.edit3NextButton.show()

        self.edit3BeforeLabel = QLabel('Before cut angle judgments', self)
        self.edit3BeforeLabel.move(10, 10)
        self.edit3BeforeLabel.resize(labSize)
        self.edit3BeforeLabel.setFont(self.Arial12Font)
        self.edit3BeforeLabel.setAlignment(self.al)
        self.edit3BeforeLabel.show()

        self.edit3AccuracyLabel = QLabel('Accuracy angle judgments', self)
        self.edit3AccuracyLabel.move(10, 150)
        self.edit3AccuracyLabel.resize(labSize)
        self.edit3AccuracyLabel.setFont(self.Arial12Font)
        self.edit3AccuracyLabel.setAlignment(self.al)
        self.edit3AccuracyLabel.show()

        self.edit3AfterLabel = QLabel('After cut angle judgments', self)
        self.edit3AfterLabel.move(10, 290)
        self.edit3AfterLabel.resize(labSize)
        self.edit3AfterLabel.setFont(self.Arial12Font)
        self.edit3AfterLabel.setAlignment(self.al)
        self.edit3AfterLabel.show()

        self.edit3TimeLabel = QLabel('Time dependency judgments', self)
        self.edit3TimeLabel.move(10, 430)
        self.edit3TimeLabel.resize(labSize)
        self.edit3TimeLabel.setFont(self.Arial12Font)
        self.edit3TimeLabel.setAlignment(self.al)
        self.edit3TimeLabel.show()

        self.edit3BeforeList = QListWidget(self)
        self.edit3BeforeListUpdate()
        self.edit3BeforeList.move(10, 30)
        self.edit3BeforeList.resize(listSize)
        self.edit3BeforeList.show()

        self.edit3AccList = QListWidget(self)
        self.edit3AccListUpdate()
        self.edit3AccList.move(10, 170)
        self.edit3AccList.resize(listSize)
        self.edit3AccList.show()

        self.edit3AfterList = QListWidget(self)
        self.edit3AfterListUpdate()
        self.edit3AfterList.move(10, 310)
        self.edit3AfterList.resize(listSize)
        self.edit3AfterList.show()

        self.edit3TimeList = QListWidget(self)
        self.edit3TimeListUpdate()
        self.edit3TimeList.move(10, 450)
        self.edit3TimeList.resize(listSize)
        self.edit3TimeList.show()

        self.edit3DeleteBeforeButton = QPushButton('Delete Judgment', self)
        self.edit3DeleteBeforeButton.move(660, 100)
        self.edit3DeleteBeforeButton.resize(butSize)
        self.edit3DeleteBeforeButton.clicked.connect(
            lambda: self.deleteJudgment('beforeCutAngleJudgments', self.edit3BeforeList.currentRow()))
        self.edit3DeleteBeforeButton.show()

        self.edit3DeleteAccButton = QPushButton('Delete Judgment', self)
        self.edit3DeleteAccButton.move(660, 240)
        self.edit3DeleteAccButton.resize(butSize)
        self.edit3DeleteAccButton.clicked.connect(lambda:
                                                  self.deleteJudgment('accuracyJudgments',
                                                                      self.edit3AccList.currentRow()))
        self.edit3DeleteAccButton.show()

        self.edit3DeleteAfterButton = QPushButton('Delete Judgment', self)
        self.edit3DeleteAfterButton.move(660, 380)
        self.edit3DeleteAfterButton.resize(butSize)
        self.edit3DeleteAfterButton.clicked.connect(lambda:
                                                    self.deleteJudgment('afterCutAngleJudgments',
                                                                        self.edit3AfterList.currentRow()))
        self.edit3DeleteAfterButton.show()

        self.edit3DeleteTimeButton = QPushButton('Delete Judgment', self)
        self.edit3DeleteTimeButton.move(660, 520)
        self.edit3DeleteTimeButton.resize(butSize)
        self.edit3DeleteTimeButton.clicked.connect(lambda:
                                                   self.deleteJudgment('timeDependencyJudgments',
                                                                       self.edit3TimeList.currentRow()))
        self.edit3DeleteTimeButton.show()

        self.edit3EditBeforeButton = QPushButton('Edit Judgment', self)
        self.edit3EditBeforeButton.move(660, 70)
        self.edit3EditBeforeButton.resize(butSize)
        self.edit3EditBeforeButton.clicked.connect(lambda:
                                                   self.edit3EditJudClick('beforeCutAngleJudgments',
                                                                          self.edit3BeforeList.currentRow()))
        self.edit3EditBeforeButton.show()

        self.edit3NewBeforeButton = QPushButton('New Judgment', self)
        self.edit3NewBeforeButton.move(660, 40)
        self.edit3NewBeforeButton.resize(butSize)
        self.edit3NewBeforeButton.clicked.connect(lambda:
                                                  self.edit3NewJudClick('beforeCutAngleJudgments'))
        self.edit3NewBeforeButton.show()

        self.edit3EditAccButton = QPushButton('Edit Judgment', self)
        self.edit3EditAccButton.move(660, 210)
        self.edit3EditAccButton.resize(butSize)
        self.edit3EditAccButton.clicked.connect(lambda:
                                                self.edit3EditJudClick('accuracyJudgments',
                                                                       self.edit3AccList.currentRow()))
        self.edit3EditAccButton.show()

        self.edit3NewAccButton = QPushButton('New Judgment', self)
        self.edit3NewAccButton.move(660, 180)
        self.edit3NewAccButton.resize(butSize)
        self.edit3NewAccButton.clicked.connect(lambda:
                                               self.edit3NewJudClick('accuracyJudgments'))
        self.edit3NewAccButton.show()

        self.edit3EditAfterButton = QPushButton('Edit Judgment', self)
        self.edit3EditAfterButton.move(660, 350)
        self.edit3EditAfterButton.resize(butSize)
        self.edit3EditAfterButton.clicked.connect(lambda:
                                                  self.edit3EditJudClick('afterCutAngleJudgments',
                                                                         self.edit3AfterList.currentRow()))
        self.edit3EditAfterButton.show()

        self.edit3NewAfterButton = QPushButton('New Judgment', self)
        self.edit3NewAfterButton.move(660, 320)
        self.edit3NewAfterButton.resize(butSize)
        self.edit3NewAfterButton.clicked.connect(lambda:
                                                 self.edit3NewJudClick('afterCutAngleJudgments'))
        self.edit3NewAfterButton.show()

        self.edit3EditTimeButton = QPushButton('Edit Judgment', self)
        self.edit3EditTimeButton.move(660, 460)
        self.edit3EditTimeButton.resize(butSize)
        self.edit3EditTimeButton.clicked.connect(lambda:
                                                 self.edit3EditJudClick('timeDependencyJudgments',
                                                                        self.edit3TimeList.currentRow()))
        self.edit3EditTimeButton.show()

        self.edit3NewTimeButton = QPushButton('New Judgment', self)
        self.edit3NewTimeButton.move(660, 490)
        self.edit3NewTimeButton.resize(butSize)
        self.edit3NewTimeButton.clicked.connect(lambda:
                                                self.edit3NewJudClick('timeDependencyJudgments'))
        self.edit3NewTimeButton.show()

    def deleteJudgment(self, judType, ind=0):
        if len(self.conf[judType]) == 0:
            return
        deleteWarning = QMessageBox(self)
        deleteWarning.setText('Are you sure you want to delete this judgment ?')
        if 'threshold' not in self.conf[judType][ind]:
            deleteWarning.setWindowTitle('Deleting Else')
        else:
            deleteWarning.setWindowTitle('Deleting ' + str(self.conf[judType][ind]['threshold']))
        deleteWarning.setIcon(QMessageBox.Warning)
        deleteWarning.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        deleteWarning.setDefaultButton(QMessageBox.Cancel)
        deleteWarning.buttonClicked.connect(lambda x: self.deleteJudgmentOkClick(x, judType, ind))
        deleteWarning.show()

    def deleteJudgmentOkClick(self, button, judType, ind):
        if button.text() == 'OK':
            self.conf[judType].pop(ind)
            self.conf[judType] = threSort(self.conf[judType])
            self.editScene3()

    def edit3BeforeListUpdate(self):
        self.edit3BeforeList.clear()
        self.conf['beforeCutAngleJudgments'] = threSort(self.conf['beforeCutAngleJudgments'])
        for item in self.conf['beforeCutAngleJudgments']:
            if 'threshold' not in item:
                qitem = QListWidgetItem('Else')
            else:
                qitem = QListWidgetItem(str(item['threshold']))
            qitem.setFont(self.Arial12FontNB)
            self.edit3BeforeList.addItem(qitem)

    def edit3EditJudClick(self, judType, ind=0):
        if len(self.conf[judType]) == 0:
            return
        self.cutConfWin = cutJudgmentsConfig(self.conf, ind, judType, dark_mode)
        self.cutConfWin.confirmButton.clicked.connect(self.edit3EditJudConfClick)

    def edit3EditJudConfClick(self):
        dat = self.cutConfWin.checkData()
        if dat:
            self.conf = self.cutConfWin.get_conf()
            self.editScene3()

    def edit3NewJudClick(self, judType):
        self.conf[judType].append({"text": ""})
        self.cutConfWin = cutJudgmentsConfig(self.conf, -1, judType, dark_mode, True)
        self.cutConfWin.confirmButton.clicked.connect(self.edit3EditJudConfClick)

    def edit3AccListUpdate(self):
        self.edit3AccList.clear()
        self.conf['accuracyJudgments'] = threSort(self.conf['accuracyJudgments'])
        for item in self.conf['accuracyJudgments']:
            if 'threshold' not in item:
                qitem = QListWidgetItem('Else')
            else:
                qitem = QListWidgetItem(str(item['threshold']))
            qitem.setFont(self.Arial12FontNB)
            self.edit3AccList.addItem(qitem)

    def edit3AfterListUpdate(self):
        self.edit3AfterList.clear()
        self.conf['afterCutAngleJudgments'] = threSort(self.conf['afterCutAngleJudgments'])
        for item in self.conf['afterCutAngleJudgments']:
            if 'threshold' not in item:
                qitem = QListWidgetItem('Else')
            else:
                qitem = QListWidgetItem(str(item['threshold']))
            qitem.setFont(self.Arial12FontNB)
            self.edit3AfterList.addItem(qitem)

    def edit3TimeListUpdate(self):
        self.edit3TimeList.clear()
        self.conf['timeDependencyJudgments'] = threSort(self.conf['timeDependencyJudgments'])
        for item in self.conf['timeDependencyJudgments']:
            if 'threshold' not in item:
                qitem = QListWidgetItem('Else')
            else:
                qitem = QListWidgetItem(str(item['threshold']))
            qitem.setFont(self.Arial12FontNB)
            self.edit3TimeList.addItem(qitem)

    def edit3BackClick(self):
        self.saveToFile()
        self.hideAll()
        self.editScene2()

    def edit3NextClick(self):
        self.saveToFile()
        self.backToMenuButtonClick()

    def edit2delThrClick(self):
        if self.thresholdList.currentItem():
            deleteWarning = QMessageBox(self)
            deleteWarning.setText('Are you sure you want to delete this judgment ?')
            deleteWarning.setWindowTitle('Deleting ' + self.thresholdList.currentItem().text())
            deleteWarning.setIcon(QMessageBox.Warning)
            deleteWarning.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            deleteWarning.setDefaultButton(QMessageBox.Cancel)
            deleteWarning.buttonClicked.connect(lambda x: self.edit2DelMsgClick(x))
            deleteWarning.show()

    def edit2DelMsgClick(self, button):
        if button.text() == 'OK':
            self.conf['judgments'].pop(self.thresholdList.currentRow())
            self.thresholdList.takeItem(self.thresholdList.currentRow())
            self.conf['judgments'] = threSort(self.conf['judgments'])
            self.editScene2()

    def refreshClick(self):
        self.setConfList()


sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback_e):
    sys.__excepthook__(exctype, value, traceback_e)
    with open('Settings/Logs/crash-report.log', 'a+') as cr:
        traceback.print_exception(exctype, value, traceback_e, file=cr)
    sys.exit(1)


sys.excepthook = my_exception_hook


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
