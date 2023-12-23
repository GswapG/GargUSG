import sys
from PyQt5.QtWidgets import( 
    QApplication, 
    QDialog, 
    QVBoxLayout, 
    QHBoxLayout,
    QPushButton, 
    QLabel
)
from PyQt5.QtGui import QIcon

class ConfirmDialog(QDialog):
    def __init__(self,first,last,number):
        super().__init__()
        self.first = first
        self.last = last
        self.number = number
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Confirmation")
        self.setWindowIcon(QIcon('logo.png'))
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        label = QLabel(f"Filling {self.number} form(s) from '{self.first}' to '{self.last}', do you wish to proceed?")
        layout.addWidget(label)

        btn_ok = QPushButton("OK", self)
        btn_cancel = QPushButton("Cancel", self)

        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)

        button_layout.addWidget(btn_ok)
        button_layout.addWidget(btn_cancel)
        layout.addLayout(button_layout)
        self.setLayout(layout)

def calling_function():
    app = QApplication(sys.argv)
    dialog = ConfirmDialog()

    if dialog.exec_() == QDialog.Accepted:
        print("Proceed with execution")
    else:
        print("Execution halted")

    sys.exit(app.exec_())

if __name__ == '__main__':
    calling_function()
