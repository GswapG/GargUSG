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
        self.button = QPushButton("Load Patient Data")
        self.button.clicked.connect(self.load_data)
        ##Layout
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        layout.addWidget(self.button)
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



#Driver
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    app.exec()