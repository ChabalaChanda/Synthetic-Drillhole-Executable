
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
import sys

from CustomFunctionClass import MakeFilesClass
 
class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI,self).__init__()
		
        loadUi("main_gui.ui",self)

        try:
            makeFilesClass = MakeFilesClass()
            self.pushButton_createFiles.clicked.connect(lambda:makeFilesClass.createFiles(self))
            self.probability_horizontalSlider.valueChanged.connect(lambda:makeFilesClass.myvalueChanged(self))
            self.actionCreate_Holes_In_Datamine.triggered.connect(lambda:makeFilesClass.createDMFiles(self))
        except:
            with open("error.txt", mode='w', newline='') as file:
                file.write('something went wrong')
                file.close()
            

if __name__ == "__main__":
	app = QApplication(sys.argv)
	ui = MainUI()
	ui.show()
	app.exec_()
