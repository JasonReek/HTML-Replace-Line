import sys
import os  

from PySide2.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QComboBox, QVBoxLayout, QLineEdit, QTextEdit, QMessageBox, QScroller, QScrollArea,
                               QTabWidget, QSizePolicy, QAction, QFileDialog, QPushButton, QGridLayout, QCheckBox, QSpinBox, QFrame)
from PySide2.QtCore import (Qt, QSize, QRect, QCoreApplication)
from PySide2.QtGui import (QIcon, QFont,  QImageWriter)


class Window(QMainWindow):
    def __init__(self):
        # Application Settings:
        self.app = QApplication(sys.argv)
        self.app.setStyle("Fusion")
        #self.app.setWindowIcon(QIcon("gear_drop.ico"))
        super(Window, self).__init__()
        self.setWindowTitle("Nerd Lab - HTML Replace")
        self.main_widget = QWidget(self)
        self.main_layout = QGridLayout(self.main_widget)
        self.setStyleSheet("background-color: #333333; color: #dedede;")

        self.exit_command = QAction("Exit", self)
        self.exit_command.triggered.connect(self.close)

        self.main_menu = self.menuBar()
        self.file_menu = self.main_menu.addMenu("File")
        self.file_menu.addAction(self.exit_command)
        self.help_menu = self.main_menu.addMenu("Help") 

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_widget)
        QScroller.grabGesture(self.scroll_area.viewport(), QScroller.LeftMouseButtonGesture)

        html_dir_row = QWidget()
        html_dir_layout = QGridLayout(html_dir_row)
        self.html_dir_label = QLabel("Directory containing the Html files:")
        self.html_dir_entry = QLineEdit()
        self.html_dir_entry.setStyleSheet("background-color: #434343; selection-background-color: darkgray;")
        self.html_dir_entry.setReadOnly(True)
        self.html_dir_entry.setCursor(Qt.IBeamCursor)
        self.html_dir_button = QPushButton("Browse")
        self.html_dir_button.clicked.connect(self.setHTMLDir)
        html_dir_layout.addWidget(self.html_dir_label, 0, 0)
        html_dir_layout.addWidget(self.html_dir_entry, 1, 0)
        html_dir_layout.addWidget(self.html_dir_button, 1, 1)

        self.html_files = []
        self.dir_name = "Replaced Html Files"

        self.scroll_layout = QGridLayout(self.scroll_widget)
        
        self.add_replace_button = QPushButton("Add Replace Entry")
        self.add_replace_button.clicked.connect(self.addReplaceRow)
        self.rmv_replace_button = QPushButton("Remove Replace Entry")
        self.rmv_replace_button.clicked.connect(self.removeReplaceRow)
        replace_button_row = QWidget()
        replace_button_row_layout = QGridLayout(replace_button_row)
        replace_button_row_layout.addWidget(self.add_replace_button, 0, 0)
        replace_button_row_layout.addWidget(self.rmv_replace_button, 0, 1)
        replace_button_row_layout.addWidget(self.filler(False), 0, 2)

        self.status_box = QTextEdit()
        self.status_box.setReadOnly(True)
        self.status_box.setCursor(Qt.IBeamCursor)
        self.status_box.setStyleSheet("background-color: #434343;")
        
        replace_row = QWidget()
        replace_layout = QGridLayout(replace_row)
        self.replace_button = QPushButton("Replace")
        self.replace_button.clicked.connect(self.replaceHTML)
        self.replace_button.setDisabled(True)
        replace_layout.addWidget(self.filler(False), 0, 0)
        replace_layout.addWidget(self.replace_button, 0, 1)
        

        self.replace_grid = QWidget()
        self.replace_grid_layout = QGridLayout(self.replace_grid)
        self.current_row = 0
        self.scroll_layout.addWidget(self.replace_grid)
        self.scroll_layout.addWidget(self.filler())

        self.main_layout.addWidget(html_dir_row)
        self.main_layout.addWidget(QLabel('Enter the exact line of Html you want to replace in the "Find What:" entry.\nIn the "Replace With:" entry, enter the Html that will be replacing the found line of Html.'))
        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(replace_button_row)
        self.main_layout.addWidget(self.status_box)
        self.main_layout.addWidget(replace_row)
        
        

        self.setCentralWidget(self.main_widget)
        

        self.replace_rows = []
        self.addReplaceRow()
        self.rmv_replace_button.setDisabled(True)
        self.createReplaceFolder()
        
    def start(self):
        self.showMaximized()
        sys.exit(self.app.exec_())
    
    def createReplaceFolder(self):
        try:
            if os.path.isdir(self.dir_name):
                for html_file in os.listdir(self.dir_name):
                    os.remove(self.dir_name+'/'+html_file)
            else:
                os.mkdir(self.dir_name)
            
        except Exception as e:
            print(str(e)+" on line {}".format(sys.exc_info()[-1].tb_lineno))

    def setHTMLDir(self):
        try:
            html_dir = QFileDialog.getExistingDirectory()
            if html_dir != "":
                self.html_dir_entry.setText(html_dir)
                self.replace_button.setEnabled(True)

        except Exception as e:
            print(str(e)+" on line {}".format(sys.exc_info()[-1].tb_lineno))

    def replaceHTML(self):
        try:
            extension = ""  
            html_dir_path = self.html_dir_entry.text()
            first_line = True
            replace_count = 0
            self.status_box.clear() 
            if html_dir_path != "":
                self.html_files = list(os.listdir(html_dir_path))
                for i in range(0, len(self.html_files)):
                    extension = os.path.splitext(self.html_files[i])[1]
                    if extension == ".html" or extension == ".htm":
                        if first_line:
                            replace_count = self.replaceHTMLInFile(self.html_files[i])
                            self.status_box.insertHtml(self.html_files[i]+"  <b>"+str(replace_count)+"</b> lines replaced.")
                            first_line = False 
                        else:
                            replace_count = self.replaceHTMLInFile(self.html_files[i])
                            self.status_box.insertHtml("<br />"+self.html_files[i]+"  <b>"+str(replace_count)+"</b> lines replaced.")
        
        except Exception as e:
            print(str(e)+" on line {}".format(sys.exc_info()[-1].tb_lineno))
    
    def findLineInHTML(self, html_line):
        for replace_row in self.replace_rows:
            replace_html_line =  replace_row[1].text()
            replace_html_line = replace_html_line.strip()
            if html_line == replace_html_line:
                new_line = replace_row[3].text()
                return new_line.strip()
        return ""

    def replaceHTMLInFile(self, html_file):
        try:
            replace_html_line = ""
            replace_counts = 0
            with open(self.html_dir_entry.text()+'/'+html_file, 'r', encoding='UTF-8') as h_f, open(self.dir_name+'/'+html_file, 'w', encoding='UTF-8') as new_h_f:
                for line in h_f:
                    replace_html_line = self.findLineInHTML(line.strip())
                    if replace_html_line == "":
                        new_h_f.write(line)
                    else:
                        new_h_f.write(replace_html_line)
                        replace_counts += 1

            return replace_counts
                    
        
        except Exception as e:
            print(str(e)+" on line {}".format(sys.exc_info()[-1].tb_lineno))

    def addReplaceRow(self):
        try:
            replace_row = [QLabel(str(self.current_row+1)+")  Find What: "), QLineEdit(), QLabel("   Replace With: "), QLineEdit()]
            replace_row[1].setStyleSheet("background-color: #434343; selection-background-color: darkgray;")
            replace_row[3].setStyleSheet("background-color: #434343; selection-background-color: darkgray;")
            column = 0
            for widget in replace_row:
                self.replace_grid_layout.addWidget(widget, self.current_row, column)
                column += 1
            
            self.replace_rows.append(replace_row)
            self.current_row += 1
            if len(self.replace_rows) > 1:
                self.rmv_replace_button.setEnabled(True) 

        except Exception as e:
            print(str(e)+" on line {}".format(sys.exc_info()[-1].tb_lineno))
    
    def removeReplaceRow(self):
        try:
            if len(self.replace_rows) > 1:
                for widget in self.replace_rows[len(self.replace_rows)-1]:
                    self.replace_grid_layout.removeWidget(widget)
                    widget.deleteLater()

                del self.replace_rows[len(self.replace_rows)-1]
                self.current_row -= 1
                if len(self.replace_rows) == 1:
                    self.rmv_replace_button.setDisabled(True) 

        except Exception as e:
            print(str(e)+" on line {}".format(sys.exc_info()[-1].tb_lineno))
    
    def filler(self, vertical_filler=True):
        filler = QWidget()
        if vertical_filler:
            filler.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            return filler
        filler.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        return filler
    
    def breakLine(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

if __name__ == "__main__":
    window = Window()
    window.start()