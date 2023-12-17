from PyQt5.QtWidgets import(
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QWidget
)
from PyQt5.QtCore import QSize
import sys

#Mainwindow 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ##Window properties
        minSize = QSize(1000,800) #Change to change minimum window size
        self.setWindowTitle("PyariBitiya Form F")
        self.setMinimumSize(minSize)

        ##Widgets




#Driver
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()