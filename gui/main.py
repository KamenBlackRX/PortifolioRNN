import sys, signal
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile, Qt
from PySide2.QtWidgets import QMainWindow, QPushButton, QApplication, QMdiArea, QMessageBox




class MainWindow(QMainWindow):

    def __init__(self, parent=None, title="Morpheus MachineLearning Studio"):        
        print("Initializing Qt structure")
        super(MainWindow, self).__init__(parent)

        signal.signal(signal.SIGINT, self.reciveSignalfromOs)

    def reciveSignalfromOs(self,frame, signal):
        msg = QMessageBox(self)
        msg.show(self)
        # This will be held to exit forom program
        if msg.accept():
            exit(1)
    
    def loadUi(self, nameOfUi = "main.ui"):
        ui = QFile(nameOfUi)
        ui.open(QFile.ReadOnly)
        loader = QUiLoader()
        window = loader.load(ui)
        if nameOfUi == "main.ui":
            self.mainwindow = window
        return window
    
    def loadMDIWindow(self, mainWindow=None, targetWindow=None):
        assert mainWindow, "Main window can't be none"
        assert targetWindow, "Target window can't be none"
        
        mdiWindow = self.loadUi(targetWindow)
        mainWindow.mdiMainWindow.addSubWindow(mdiWindow)
        mainWindow.mdiMainWindow.showMaximized()

    def keyPressEvent(self, event):
        super(MainWindow, self).keyPressEvent(event)
        self.keyPressed.emit(event) 

    def on_key(self, event):
        if event.key() == Qt.Key_Escape:
            print("Im Escaped")
            self.proceed()  # this is called whenever the continue button is pressed
        elif event.key() == Qt.Key_C:
            print("Pressed C ")
            self.mainwindow.loadMDIWindow(mainWindow=self.mainwindow, targetWindow="form_classify.ui") # Use to openwindow


def main():
    app = QApplication(sys.argv)
    mw = MainWindow()
    mainwin = mw.loadUi()
   
    mw.loadMDIWindow(mainWindow=mainwin, targetWindow="form_classify.ui")
    mainwin.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
