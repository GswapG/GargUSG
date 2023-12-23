import pickle
import os,sys
from PyQt5.QtWidgets import(
    QDialog, 
    QVBoxLayout, 
    QHBoxLayout, 
    QLabel, 
    QLineEdit, 
    QPushButton
)
from PyQt5.QtCore import QSize

def get_credentials_path(filename):
    """ Get the path to the credentials file, works for both dev and bundled app """
    if getattr(sys, 'frozen', False):
        # We are running in a PyInstaller bundle
        # Use a user directory (e.g., appdata, home directory)
        base_path = os.path.join(os.path.expanduser('~'), 'GargGUCFormFiller')
    else:
        # We are running in a normal Python environment
        base_path = os.path.dirname(os.path.abspath(__file__))

    # Ensure base_path exists
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    # Path to credentials.bin
    return os.path.join(base_path, filename)

def credentials_exist(file_path):
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

def create_credentials(filename):
    dialog = CredentialDialog()
    if dialog.exec_() == QDialog.Accepted:
        login_id, password = dialog.getInputs()
        login_id = str(login_id).strip()
        password = str(password).strip()
        dump_credentials((login_id,password),filename)
        return True
    else:
        return False