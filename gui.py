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
    QSizePolicy
)
from PyQt5.QtCore import QSize, Qt
import sys
import openpyxl
import form_filler
import excel_assist
from datetime import datetime

path_to_excel = ".\\PNDT excel report NOVEMBER 2023.xlsm"
path_to_stylesheet = '.\stylesheet.css'
starting_row = 0
ending_row = 0
username = '102237'
password = 'flutrol70g'

#Mainwindow 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        global path_to_excel
        ##Window properties
        minSize = QSize(1000,800) #Change to change minimum window size
        self.setWindowTitle("PyariBitiya Form F")
        self.setMinimumSize(minSize)

        ##Widgets
        self.central_widget = QWidget()
        self.table_widget = QTableWidget()
        self.load_button = QPushButton('Load Patient Data')
        self.load_button.clicked.connect(self.load_data)
        self.select_button = QPushButton('Grab selected rows')
        self.select_button.clicked.connect(self.grab_rows)
        self.fill_form_button = QPushButton('Fill Forms')
        self.fill_form_button.clicked.connect(self.fill_forms)
        self.change_file_button = QPushButton('Change Excel File')
        self.change_file_button.clicked.connect(self.change_excel_file)
        ##Layout
        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout2.addWidget(self.table_widget)
        layout1.addWidget(self.load_button)
        layout1.addWidget(self.select_button)
        layout1.addWidget(self.change_file_button)
        layout1.addWidget(self.fill_form_button)
        layout2.addLayout(layout1)
        self.central_widget.setLayout(layout2)
        

        self.setCentralWidget(self.central_widget)
        path_to_excel , _ = QFileDialog.getOpenFileName(self, "Open PNDT Excel File","", "Excel Files (*.xls*)")



    def load_data(self):
        workbook = openpyxl.load_workbook(path_to_excel)
        sheet = workbook.active

        self.table_widget.setColumnCount(6)
        column_headers = ['Index','Date','Patient Name','W/o D/o','Age','Address and Phone']
        list_values = list(sheet.values)
        self.table_widget.setHorizontalHeaderLabels(column_headers)
        display_values = excel_assist.convert_to_format(list_values)
        display_values = excel_assist.filter(display_values,path_to_excel)
        self.table_widget.setRowCount(len(display_values))
        row_index = 0
        for value_tuple in display_values:
            date = str(value_tuple[1])
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            date = date.strftime('%d-%m-%Y')
            index_item = QTableWidgetItem(str(value_tuple[0]))
            date_item = QTableWidgetItem(date)
            patient_item = QTableWidgetItem(str(value_tuple[2]))
            husband_item = QTableWidgetItem(str(value_tuple[4]))
            age_item = QTableWidgetItem(str(value_tuple[3]))
            address_item = QTableWidgetItem(str(value_tuple[5]))
            index_item.setFlags(index_item.flags() & ~Qt.ItemIsEditable)
            date_item.setFlags(date_item.flags() & ~Qt.ItemIsEditable)
            patient_item.setFlags(patient_item.flags() & ~Qt.ItemIsEditable)
            husband_item.setFlags(husband_item.flags() & ~Qt.ItemIsEditable)
            age_item.setFlags(age_item.flags() & ~Qt.ItemIsEditable)
            address_item.setFlags(age_item.flags() & ~Qt.ItemIsEditable)
            self.table_widget.setItem(row_index,0,index_item)
            self.table_widget.setItem(row_index,1,date_item)
            self.table_widget.setItem(row_index,2,patient_item)
            self.table_widget.setItem(row_index,3,husband_item)
            self.table_widget.setItem(row_index,4,age_item)
            self.table_widget.setItem(row_index,5,address_item)
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
        ending_row = self.table_widget.item(ending_index,0).text()
        starting_row = self.table_widget.item(starting_index,0).text()

    def grab_all(self):
        global ending_row
        global starting_row

        starting_row = self.table_widget.item(0,0).text()
        ending_row = self.table_widget.item(self.table_widget.rowCount()-2,0).text()
        print(ending_row)

    def fill_forms(self):
        helper = form_filler.filler_helper()
        helper.login(username,password)

    def change_excel_file(self):
        global path_to_excel
        path_to_excel , _ = QFileDialog.getOpenFileName(self, "Open PNDT Excel File","", "Excel Files (*.xls*)")
        self.load_data()


#Driver
if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open(path_to_stylesheet, 'r') as file:
        app.setStyleSheet(file.read())
    window = MainWindow()
    window.showMaximized()
    app.exec()