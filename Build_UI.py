'''
Author: Cabrite
Date: 2020-10-28 21:36:51
LastEditors: Cabrite
LastEditTime: 2020-10-30 20:10:58
Description: Do not edit
'''
import sys
import platform
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from EassyReading import Ui_MainWindow
import GenerateSentence
import Resrouces_rc


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("论文阅读")
        self.setWindowIcon(QIcon(':/Icons/Resources/document_128px_1287920_easyicon.net.ico'))
        GenerateSentence.setupUIFunctions(self)

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

 