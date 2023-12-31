from PyQt5.QtWidgets import(
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
    QDialog
)
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon
import sys, os
import openpyxl
import form_filler
import excel_assist
import gui_utils
import credential_manager
from datetime import datetime

try: 
  from ctypes import windll # Only exists on Windows.
  myappid = "com.gargGUC.pyaribitiya.automaticformfiller.1" 
  windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
  pass

path_to_excel = "PNDT excel report NOVEMBER 2023.xlsm"
stylesheet = 'stylesheet.css'
credentials_filename = 'credentials.bin'
credentials_path = credential_manager.get_credentials_path(credentials_filename)
starting_row = 3
ending_row = 3
done_with_credentials = True
username = ''
password = ''

def resource_path(relative_path):
    base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

if credential_manager.credentials_exist(credentials_path):
    username, password = credential_manager.get_credentials(credentials_path)



#Mainwindow 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        global username
        global password
        global path_to_excel
        self.list_values = []
        ##Window properties
        minSize = QSize(1000,800) #Change to change minimum window size
        self.setWindowTitle("PyariBitiya Form F")
        self.setMinimumSize(minSize)

        ##Widgets
        self.central_widget = QWidget()
        self.table_widget = QTableWidget()
        self.table_widget.itemSelectionChanged.connect(self.grab_rows)
        self.credentials_button = QPushButton('Change Credentials')
        self.credentials_button.clicked.connect(self.change_credentials)
        self.select_button = QPushButton('Grab selected rows')
        self.select_button.clicked.connect(self.grab_rows)
        self.fill_form_button = QPushButton('Fill Forms')
        self.fill_form_button.clicked.connect(self.fill_forms)
        self.change_file_button = QPushButton('Change Excel File')
        self.change_file_button.clicked.connect(self.change_excel_file)
        self.label = QLabel()
        pixmap = QPixmap(resource_path('girl_logo.png'))
        pixmap = pixmap.scaled(int(pixmap.width()/2.4), int(pixmap.height()/2.4))
        self.label.setPixmap(pixmap)
        ##Layout
        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout2.addWidget(self.table_widget)
        # layout1.addWidget(self.load_button)
        # layout1.addWidget(self.select_button)
        layout1.addWidget(self.label)
        layout1.addWidget(self.credentials_button)
        layout1.addWidget(self.change_file_button)
        layout1.addWidget(self.fill_form_button)
        layout2.addLayout(layout1)
        self.central_widget.setLayout(layout2)
        

        self.setCentralWidget(self.central_widget)
        self.showMaximized()
        flag = True
        while flag:
            if not credential_manager.credentials_exist(credentials_path):
                QMessageBox.warning(self, "WARNING", "You need to enter login credentials as they do not exist!")
                if credential_manager.create_credentials(credentials_path):
                    flag = False
                    username, password = credential_manager.get_credentials(credentials_path)
                else:
                    QMessageBox.warning(self, "WARNING", "You need to enter login credentials as they do not exist!")
            else:
                flag = False

        try:
            flag = True
            while flag:
                path_to_excel , _ = QFileDialog.getOpenFileName(self, "Open PNDT Excel File","", "Excel Files (*.xls*)")
                if excel_assist.validate_path(path_to_excel):
                    flag = False
                else:
                    QMessageBox.warning(self, "Warning", "Please select a valid PNDT file!!")
            self.load_data()
        except:
            QMessageBox.warning(self, "Warning", "Please select excel file to load data")
            self.change_excel_file()

    def load_data(self):
        workbook = openpyxl.load_workbook(path_to_excel)
        sheet = workbook.active

        self.table_widget.setColumnCount(7)
        column_headers = ['Index','Date','Patient Name','W/o D/o','Age','Address and Phone','Excel Index']
        self.table_widget.setHorizontalHeaderLabels(column_headers)
        self.list_values = list(sheet.values)

        self.display_values = excel_assist.convert_to_format(self.list_values)
        self.display_values = excel_assist.filter(self.display_values,path_to_excel)
        self.table_widget.setRowCount(len(self.display_values))
        row_index = 0
        for value_tuple in self.display_values:
            date = str(value_tuple[1])
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            date = date.strftime('%d/%m/%Y')
            index_item = QTableWidgetItem(str(value_tuple[0]))
            date_item = QTableWidgetItem(date)
            patient_item = QTableWidgetItem(str(value_tuple[2]))
            husband_item = QTableWidgetItem(str(value_tuple[4]))
            age_item = QTableWidgetItem(str(value_tuple[3]))
            address_item = QTableWidgetItem(str(value_tuple[5]))
            row_index_item = QTableWidgetItem(str(value_tuple[-1]))
            index_item.setFlags(index_item.flags() & ~Qt.ItemIsEditable)
            date_item.setFlags(date_item.flags() & ~Qt.ItemIsEditable)
            patient_item.setFlags(patient_item.flags() & ~Qt.ItemIsEditable)
            husband_item.setFlags(husband_item.flags() & ~Qt.ItemIsEditable)
            age_item.setFlags(age_item.flags() & ~Qt.ItemIsEditable)
            address_item.setFlags(age_item.flags() & ~Qt.ItemIsEditable)
            row_index_item.setFlags(age_item.flags() & ~Qt.ItemIsEditable)
            self.table_widget.setItem(row_index,0,index_item)
            self.table_widget.setItem(row_index,1,date_item)
            self.table_widget.setItem(row_index,2,patient_item)
            self.table_widget.setItem(row_index,3,husband_item)
            self.table_widget.setItem(row_index,4,age_item)
            self.table_widget.setItem(row_index,5,address_item)
            self.table_widget.setItem(row_index,6,row_index_item)
            row_index += 1
        
        self.table_widget.resizeColumnsToContents()
        workbook.close()

    def grab_rows(self):
        global ending_row
        global starting_row

        selected_range = self.table_widget.selectedRanges()
        if selected_range:
            selected_range = selected_range[0]
        else:
            QMessageBox.warning(self, "Warning", 'No rows selected')
            return
        starting_index = selected_range.topRow()
        ending_index = selected_range.bottomRow()
        ending_row = int(self.table_widget.item(ending_index,6).text())
        starting_row = int(self.table_widget.item(starting_index,6).text())
        print(starting_row)
        print(ending_row)

    def grab_all(self):
        global ending_row
        global starting_row

        starting_row = int(self.table_widget.item(0,0).text())
        ending_row = int(self.table_widget.item(self.table_widget.rowCount()-2,0).text())
        print(ending_row)

    def fill_forms(self):
        if(ending_row <= 3 and starting_row <= 3):
            QMessageBox.warning(self, "Warning", "Please select forms to fill")
            return
        entries = excel_assist.generate_selected_entries(self.list_values,self.display_values,starting_row,ending_row)
        first_name = entries[0][2]
        last_name = entries[-1][2]
        no_of_forms = len(entries)
        dialog = gui_utils.ConfirmDialog(first_name,last_name,no_of_forms)
        if dialog.exec_() != QDialog.Accepted:
            return
        # for entry in entries:
        #     print(entry[0])
        try:
            helper = form_filler.filler_helper(self)
            helper.login(username,password)
            helper.goto_form_f()
            helper.fill_selected_forms(entries)
        except form_filler.custom_exception as ce:
            helper.close_driver()
            if(ce.message == "too long"):
                self.indicate_took_too_long()
            else:
                QMessageBox.warning(self,"WARNING!", "Chrome closed unexpectedly")
        except Exception:
            helper.close_driver()
            QMessageBox.critical(self, "WARNING", "Something went wrong while filling a form. Please check website for forms filled")

    def indicate_forms_filled(self,values):
        number_of_forms = len(values)
        first_name = values[0][2]
        last_name = values[-1][2]
        QMessageBox.information(self, 'Success!', f'Filled {number_of_forms} forms from "{first_name}" to "{last_name}"')
        
    def indicate_took_too_long(self):
        QMessageBox.warning(self, "WARNING!", "Form filling failed. Website took too long to respond.")

    def change_excel_file(self):
        global path_to_excel
        try:
            flag = True
            while flag:
                path_to_excel , _ = QFileDialog.getOpenFileName(self, "Open PNDT Excel File","", "Excel Files (*.xls*)")
                if excel_assist.validate_path(path_to_excel):
                    flag = False
                else:
                    QMessageBox.warning(self, "Warning", "Please select a valid PNDT file!!")

            self.load_data()
        except:
            QMessageBox.warning(self, "Warning", "No File Selected")
            self.change_excel_file()

    def change_credentials(self):
        global username
        global password
        if credential_manager.create_credentials(credentials_path):
            QMessageBox.information(self, "Done", "New credentials saved successfully!")
            username, password = credential_manager.get_credentials(credentials_path)
        else:
            QMessageBox.information(self, "Alright", "Still on old credentials.")
        print(username, password)

#Driver
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path('logo.png')))
    with open(resource_path(stylesheet), 'r') as file:
        app.setStyleSheet(file.read())
    window = MainWindow()
    window.showMaximized()
    app.exec()