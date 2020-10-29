from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import datetime
import os


class setupUIFunctions():
    def __init__(self, Window):
        self.Window = Window
        self.isTop = False
        self.setupUIFunctions()

    def setupUIFunctions(self):
        self.connectSignals2Slots()

    def connectSignals2Slots(self):
        self.Window.pushButton_quit.clicked.connect(lambda:self.Window.close())
        self.Window.pushButton_copy.clicked.connect(self.GenerateOutput)
        self.Window.pushButton_clear.clicked.connect(self.ClearOutput)
        self.Window.pushButton_top.clicked.connect(self.ChangeTopState)
        self.Window.pushButton_Load.clicked.connect(self.LoadinData)
        self.Window.pushButton_PasteEassy.clicked.connect(self.PasteIntoEassy)
        self.Window.pushButton_PasteAuthor.clicked.connect(self.PasteIntoAuthor)
        self.Window.pushButton_PasteModel.clicked.connect(self.PasteIntoModel)
        self.Window.pushButton_PasteKeywords.clicked.connect(self.PasteIntoKeywords)
        self.Window.pushButton_PasteComments.clicked.connect(self.PasteIntoComments)
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
        Output += self.Window.plainTextEdit_Base.toPlainText()
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
            

    def LoadinData(self):
        data = self.getClipBoard()
        if data.count('\t') != 7:
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

        self.Window.spinBox.setValue(int(data[0]))


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