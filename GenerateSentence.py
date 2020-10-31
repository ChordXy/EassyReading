from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import threading
import datetime
import time
import os


class retrieveThread(QThread):
    retrieveResult = pyqtSignal(list)

    def __init__(self, parent=None):
        super(retrieveThread, self).__init__(parent)

    def setParameters(self, folder, search_file):
        self.folder = folder
        self.search_file = (search_file + '.pdf').upper()

    def run(self):
        result = []
        for root, _, files in os.walk(self.folder):
            for file in files:
                fileup = file.upper()
                if fileup.endswith(self.search_file):
                    result.append(os.path.join(root, file))
        self.retrieveResult.emit(result)


class setupUIFunctions():
    def __init__(self, Window):
        self.Window = Window
        self.isTop = False
        self.StarState = 0
        self.WorkSpace = "C:/"
        self.reThread = retrieveThread()
        self.Window.action_I.setEnabled(False)
        self.DefaultSaveDir = os.path.join(QDir.homePath(), 'Documents', 'EassyReading.log')
        self.setupUIFunctions()

    def setupUIFunctions(self):
        self.loadParams()
        self.connectSignals2Slots()

    def connectSignals2Slots(self):
        self.Window.pushButton_star1.clicked.connect(lambda:self.LightupStars(1))
        self.Window.pushButton_star2.clicked.connect(lambda:self.LightupStars(2))
        self.Window.pushButton_star3.clicked.connect(lambda:self.LightupStars(3))
        self.Window.pushButton_star4.clicked.connect(lambda:self.LightupStars(4))
        self.Window.pushButton_star5.clicked.connect(lambda:self.LightupStars(5))

        QShortcut(QKeySequence(self.Window.tr("Ctrl+1")), self.Window, self.PasteIntoEassy)
        QShortcut(QKeySequence(self.Window.tr("Ctrl+2")), self.Window, self.PasteIntoAuthor)
        QShortcut(QKeySequence(self.Window.tr("Ctrl+3")), self.Window, self.PasteIntoModel)
        QShortcut(QKeySequence(self.Window.tr("Ctrl+4")), self.Window, self.PasteIntoKeywords)
        QShortcut(QKeySequence(self.Window.tr("Ctrl+5")), self.Window, self.PasteIntoComments)

        self.Window.action_copy.triggered.connect(self.GenerateOutput)
        self.Window.action_top.triggered.connect(self.ChangeTopState)
        self.Window.action_clear.triggered.connect(self.ClearOutput)
        self.Window.action_loadin.triggered.connect(self.LoadinData)
        self.Window.action_open.triggered.connect(self.OpenFile)
        self.Window.action_directory.triggered.connect(self.setDirectory)
        self.Window.action_I.triggered.connect(self.cancelThread)

        self.reThread.retrieveResult.connect(self.SelectFileToOpen)
        self.Window.plainTextEdit_Eassy.textChanged.connect(self.checkText)

    ####################################################################################
    #                                  Functions                                       #
    ####################################################################################
    def getClipBoard(self):
        clipboard = QApplication.clipboard()
        return clipboard.text()

    def setClipBoard(self, sentence):
        clipboard = QApplication.clipboard()
        clipboard.setText(sentence)

    def checkText(self):
        sentence = self.Window.plainTextEdit_Eassy.toPlainText()
        sentence = sentence.replace('\r\n', ' ')
        sentence = sentence.replace('\r', ' ')
        sentence = sentence.replace('\n', ' ')
        if ':' in sentence:
            Netname = sentence.split(":")[0]
            self.Window.plainTextEdit_NetName.setPlainText(Netname)
        self.Window.plainTextEdit_Eassy.textChanged.disconnect()
        self.Window.plainTextEdit_Eassy.setPlainText(sentence)
        cursor = self.Window.plainTextEdit_Eassy.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.Window.plainTextEdit_Eassy.setTextCursor(cursor)
        self.Window.plainTextEdit_Eassy.textChanged.connect(self.checkText)

    def PackInnovation(self):
        Inns = []
        if self.Window.checkBox_Input.isChecked():
            Inns.append("Input")
        if self.Window.checkBox_Proposal.isChecked():
            Inns.append("Proposal")
        if self.Window.checkBox_Architecture.isChecked():
            Inns.append("Architecture")
        if self.Window.checkBox_Module.isChecked():
            Inns.append("Module")
        if self.Window.checkBox_Backbone.isChecked():
            Inns.append("Backbone")
        if self.Window.checkBox_Convolution.isChecked():
            Inns.append("Convolution")
        if self.Window.checkBox_Pooling.isChecked():
            Inns.append("Pooling")
        if self.Window.checkBox_Classifier.isChecked():
            Inns.append("Classifier")

        if Inns:
            return "；".join(Inns)
        else:
            return ""

    def UnpackInnovation(self, Innovations):
        Inns = Innovations.split("；")
        if "Input" in Inns:
            self.Window.checkBox_Input.setChecked(True)
        if "Proposal" in Inns:
            self.Window.checkBox_Proposal.setChecked(True)
        if "Architecture" in Inns:
            self.Window.checkBox_Architecture.setChecked(True)
        if "Module" in Inns:
            self.Window.checkBox_Module.setChecked(True)
        if "Backbone" in Inns:
            self.Window.checkBox_Backbone.setChecked(True)
        if "Convolution" in Inns:
            self.Window.checkBox_Convolution.setChecked(True)
        if "Pooling" in Inns:
            self.Window.checkBox_Pooling.setChecked(True)
        if "Classifier" in Inns:
            self.Window.checkBox_Classifier.setChecked(True)

    def LightupStars(self, number):
        self.PutoutStars()
        self.StarState = number
        if number == 1:
            self.Window.pushButton_star1.setStyleSheet("border-image: url(:/Icons/Resources/red_star_256px_1075492_easyicon.net.png);")
        if number == 2:
            self.Window.pushButton_star1.setStyleSheet("border-image: url(:/Icons/Resources/red_star_256px_1075492_easyicon.net.png);")
            self.Window.pushButton_star2.setStyleSheet("border-image: url(:/Icons/Resources/red_star_256px_1075492_easyicon.net.png);")
        if number == 3:
            self.Window.pushButton_star1.setStyleSheet("border-image: url(:/Icons/Resources/red_star_256px_1075492_easyicon.net.png);")
            self.Window.pushButton_star2.setStyleSheet("border-image: url(:/Icons/Resources/red_star_256px_1075492_easyicon.net.png);")
            self.Window.pushButton_star3.setStyleSheet("border-image: url(:/Icons/Resources/red_star_256px_1075492_easyicon.net.png);")
        if number == 4:
            self.Window.pushButton_star1.setStyleSheet("border-image: url(:/Icons/Resources/red_star_256px_1075492_easyicon.net.png);")
            self.Window.pushButton_star2.setStyleSheet("border-image: url(:/Icons/Resources/red_star_256px_1075492_easyicon.net.png);")
            self.Window.pushButton_star3.setStyleSheet("border-image: url(:/Icons/Resources/red_star_256px_1075492_easyicon.net.png);")
            self.Window.pushButton_star4.setStyleSheet("border-image: url(:/Icons/Resources/red_star_256px_1075492_easyicon.net.png);")
        if number == 5:
            self.Window.pushButton_star1.setStyleSheet("border-image: url(:/Icons/Resources/red_star_256px_1075492_easyicon.net.png);")
            self.Window.pushButton_star2.setStyleSheet("border-image: url(:/Icons/Resources/red_star_256px_1075492_easyicon.net.png);")
            self.Window.pushButton_star3.setStyleSheet("border-image: url(:/Icons/Resources/red_star_256px_1075492_easyicon.net.png);")
            self.Window.pushButton_star4.setStyleSheet("border-image: url(:/Icons/Resources/red_star_256px_1075492_easyicon.net.png);")
            self.Window.pushButton_star5.setStyleSheet("border-image: url(:/Icons/Resources/red_star_256px_1075492_easyicon.net.png);")

    def PutoutStars(self):
        self.StarState = 0
        self.Window.pushButton_star1.setStyleSheet("border-image: url(:/Icons/Resources/gray_star_256px_1075532_easyicon.net.png);")
        self.Window.pushButton_star2.setStyleSheet("border-image: url(:/Icons/Resources/gray_star_256px_1075532_easyicon.net.png);")
        self.Window.pushButton_star3.setStyleSheet("border-image: url(:/Icons/Resources/gray_star_256px_1075532_easyicon.net.png);")
        self.Window.pushButton_star4.setStyleSheet("border-image: url(:/Icons/Resources/gray_star_256px_1075532_easyicon.net.png);")
        self.Window.pushButton_star5.setStyleSheet("border-image: url(:/Icons/Resources/gray_star_256px_1075532_easyicon.net.png);")

    def EncodeStar(self):
        if self.StarState == 0:
            return ""
        else:
            return '★' * self.StarState

    def DecodeStar(self, stars):
        number = stars.count('★')
        self.LightupStars(number)

    def setTitle(self):
        if self.WorkSpace:
            self.Window.setWindowTitle("论文阅读   - " + self.WorkSpace)

    def saveParams(self):
        with open(self.DefaultSaveDir, 'w+') as file:
            file.truncate(0)
            file.write(self.WorkSpace)

    def loadParams(self):
        with open(self.DefaultSaveDir, 'r+') as file:
            self.WorkSpace = file.read()
        self.setTitle()

    def getTimeInfo(self):
        return "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') + "] "

    def ZhiYunOpen(self, file):
        application = "C:\Program Files (x86)\ZhiyunTranslator\ZhiYunTranslator.exe"
        commandText = 'start "" "' + application + '" "' + file + '"'
        command = '"' + commandText + '"'
        os.system(command)

    ####################################################################################
    #                               Upside Buttons                                     #
    ####################################################################################

    def ChangeTopState(self):
        if self.isTop:
            self.Window.setWindowFlags(Qt.Widget)
            self.isTop = False
        else:
            self.Window.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.isTop = True
        self.Window.show()

    def GenerateOutput(self):
        Output = str(self.Window.spinBox.value()) + '\t'
        Output += self.Window.plainTextEdit_Author.toPlainText() + '\t'
        Output += self.Window.plainTextEdit_NetName.toPlainText() + '\t'
        Output += self.Window.plainTextEdit_Eassy.toPlainText() + '\t'
        Output += self.Window.plainTextEdit_Comments.toPlainText() + '\t'
        Output += self.Window.plainTextEdit_KeyWords.toPlainText() + '\t'
        Output += self.PackInnovation() + '\t'
        Output += self.Window.plainTextEdit_Base.toPlainText() + '\t'
        Output += self.EncodeStar()
        self.setClipBoard(Output)

    def ClearOutput(self):
        self.Window.plainTextEdit_Eassy.clear()
        self.Window.plainTextEdit_Author.clear()
        self.Window.plainTextEdit_NetName.clear()
        self.Window.plainTextEdit_Base.clear()
        self.Window.plainTextEdit_KeyWords.clear()
        self.Window.plainTextEdit_Comments.clear()

        self.Window.checkBox_Input.setChecked(False)
        self.Window.checkBox_Proposal.setChecked(False)
        self.Window.checkBox_Architecture.setChecked(False)
        self.Window.checkBox_Module.setChecked(False)
        self.Window.checkBox_Backbone.setChecked(False)
        self.Window.checkBox_Convolution.setChecked(False)
        self.Window.checkBox_Pooling.setChecked(False)
        self.Window.checkBox_Classifier.setChecked(False)

        self.PutoutStars()
            
    def LoadinData(self):
        data = self.getClipBoard()
        if data.count('\t') != 8:
            return
        data = data.split('\t')
        self.ClearOutput()
        
        if data[1]:
            self.Window.plainTextEdit_Author.setPlainText(data[1])
        if data[2]:
            self.Window.plainTextEdit_NetName.setPlainText(data[2])
        if data[3]:
            self.Window.plainTextEdit_Eassy.textChanged.disconnect()
            self.Window.plainTextEdit_Eassy.setPlainText(data[3])
            cursor = self.Window.plainTextEdit_Eassy.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.Window.plainTextEdit_Eassy.setTextCursor(cursor)
            self.Window.plainTextEdit_Eassy.textChanged.connect(self.checkText)
        if data[4]:
            self.Window.plainTextEdit_Comments.setPlainText(data[4])
        if data[5]:
            self.Window.plainTextEdit_KeyWords.setPlainText(data[5])
        if data[6]:
            self.UnpackInnovation(data[6])
        if data[7] != '\n' and data[7] != '\r' and data[7] != '\r\n':
            self.Window.plainTextEdit_Base.setPlainText(data[7])
        if data[8]:
            self.DecodeStar(data[8])

        self.Window.spinBox.setValue(int(data[0]))

    def OpenFile(self):
        Eassy = self.Window.plainTextEdit_Eassy.toPlainText().replace(':', "")
        if not Eassy:
            return
        self.reThread.setParameters(self.WorkSpace, Eassy)
        self.reThread.start()
        self.Window.action_open.setEnabled(False)
        self.Window.action_I.setEnabled(True)

    def SelectFileToOpen(self, dirs):
        if dirs:
            self.ZhiYunOpen(dirs[0])

        self.Window.action_open.setEnabled(True)
        self.Window.action_I.setEnabled(False)

    def cancelThread(self):
        self.reThread.quit()
        self.Window.action_open.setEnabled(True)
        self.Window.action_I.setEnabled(False)    

    def setDirectory(self):
        dirt = QFileDialog.getExistingDirectory(None, "请选择当前文档存放路径", "D:")
        self.WorkSpace = dirt
        self.saveParams()
        self.setTitle() 

    ####################################################################################
    #                              Downside Buttons                                    #
    ####################################################################################

    def PasteIntoEassy(self):
        self.Window.plainTextEdit_Eassy.setPlainText(self.getClipBoard())

    def PasteIntoAuthor(self):
        self.Window.plainTextEdit_Author.setPlainText(self.getClipBoard())
        cursor = self.Window.plainTextEdit_Author.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.Window.plainTextEdit_Author.setTextCursor(cursor)

    def PasteIntoModel(self):
        self.Window.plainTextEdit_Base.setPlainText(self.getClipBoard())
        cursor = self.Window.plainTextEdit_Base.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.Window.plainTextEdit_Base.setTextCursor(cursor)

    def PasteIntoKeywords(self):
        self.Window.plainTextEdit_KeyWords.setPlainText(self.getClipBoard())
        cursor = self.Window.plainTextEdit_KeyWords.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.Window.plainTextEdit_KeyWords.setTextCursor(cursor)

    def PasteIntoComments(self):
        self.Window.plainTextEdit_Comments.setPlainText(self.getClipBoard())
        cursor = self.Window.plainTextEdit_Comments.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.Window.plainTextEdit_Comments.setTextCursor(cursor)