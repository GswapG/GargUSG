from PyQt5.QtWidgets import(
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout
)
from PyQt5.QtCore import QSize, Qt
import sys
import openpyxl
import form_filler


path_to_excel = ".\\test.xlsx"
starting_row = 0
ending_row = 0

#Mainwindow 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ##Window properties
        minSize = QSize(1000,800) #Change to change minimum window size
        self.setWindowTitle("PyariBitiya Form F")
        self.setMinimumSize(minSize)

        ##Widgets
        self.central_widget = QWidget()
        self.table_widget = QTableWidget()
        self.button1 = QPushButton('Load Patient Data')
        self.button1.clicked.connect(self.load_data)
        self.button2 = QPushButton('Grab selected rows')
        self.button2.clicked.connect(self.grab_rows)
        self.button3 = QPushButton('Fill Forms')
        self.button3.clicked.connect(self.fill_forms)
        self.button4 = QPushButton('Select All')
        self.button4.clicked.connect(self.grab_all)

        ##Layout
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.button4)
        self.central_widget.setLayout(layout)
        

        self.setCentralWidget(self.central_widget)


    def load_data(self):
        workbook = openpyxl.load_workbook(path_to_excel)
        sheet = workbook.active

        self.table_widget.setRowCount(sheet.max_row)
        self.table_widget.setColumnCount(sheet.max_column)

        list_values = list(sheet.values)
        self.table_widget.setHorizontalHeaderLabels(list_values[0])

        row_index = 0
        for value_tuple in list_values[1:]:
            col_index = 0
            for value in value_tuple:
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table_widget.setItem(row_index,col_index,item)
                col_index += 1
            row_index += 1
        
        self.table_widget.resizeColumnsToContents()

    def grab_rows(self):
        global ending_row
        global starting_row

        selected_range = self.table_widget.selectedRanges()[0]
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
        pass



#Driver
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    app.exec()