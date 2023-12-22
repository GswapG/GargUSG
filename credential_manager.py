import pickle
import os
from PyQt5.QtWidgets import(
    QMessageBox,
    QDialog, 
    QVBoxLayout, 
    QHBoxLayout, 
    QLabel, 
    QLineEdit, 
    QPushButton
)
from PyQt5.QtCore import QSize

def credentials_exist(filename):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    if os.path.exists(file_path):
        return True
    else:
        return False
    
def get_credentials(file):
    with open(file, 'rb') as f:
        cred = pickle.load(f)
    return cred

def dump_credentials(cred,file):
    with open(file, 'wb') as f:
        pickle.dump(cred,f)

class CredentialDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Input Dialog")
        self.setMinimumSize(QSize(500,100))
        layout = QVBoxLayout(self)

        # Create layout for login ID
        layout_id = QHBoxLayout()
        self.label_id = QLabel("Login ID:", self)
        self.lineEdit_id = QLineEdit(self)
        layout_id.addWidget(self.label_id)
        layout_id.addWidget(self.lineEdit_id)
        layout.addLayout(layout_id)

        # Create layout for password
        layout_password = QHBoxLayout()
        self.label_password = QLabel("Password:", self)
        self.lineEdit_password = QLineEdit(self)
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        layout_password.addWidget(self.label_password)
        layout_password.addWidget(self.lineEdit_password)
        layout.addLayout(layout_password)

        # Buttons
        self.buttons = QHBoxLayout()
        self.ok_button = QPushButton('OK', self)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        self.buttons.addWidget(self.ok_button)
        self.buttons.addWidget(self.cancel_button)
        layout.addLayout(self.buttons)

    def getInputs(self):
        return self.lineEdit_id.text(), self.lineEdit_password.text()

def create_credentials(parent_window,filename):
    dialog = CredentialDialog()
    if dialog.exec_() == QDialog.Accepted:
        login_id, password = dialog.getInputs()
        login_id = str(login_id).strip()
        password = str(password).strip()
        dump_credentials((login_id,password),filename)
        return True
    else:
        return False