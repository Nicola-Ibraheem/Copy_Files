from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUiType

import shutil as sh
import sys
import os
import logging
import re
from datetime import datetime
import json

from File_Path import File


# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

# file_handler = logging.FileHandler(filename="operations.log",mode='w')
# logger.addHandler(file_handler)

# formatter = logging.Formatter("%(asctime)s:%(filename)s:%(funcName)s:%(message)s")
# file_handler.setFormatter(formatter)


from CopyGUI import Ui_MainWindow as Copygui_
# Copygui_,_ = loadUiType("copyGUI.ui")

class Main_GUI(QtWidgets.QMainWindow,Copygui_):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Copy files")
        
        self.file = File()
       
        self.GUI_changes()
        self.handle_buttons()

    def GUI_changes(self):
        
        # self.doAnim()
        self.timer()
        # hide tabs in tabwidget
        self.tabWidget.tabBar().setVisible(False)
        self.tabWidget.setCurrentIndex(0)

        self.src_path_comboBox.addItems(self.file.source_paths)
        self.dest_path_comboBox.addItems(self.file.destination_paths)

        self.show_src_dest_paths()
        


    def handle_buttons(self):
        
        self.src_path_comboBox.activated['QString'].connect(self.show_src_files)
        self.dest_path_comboBox.activated['QString'].connect(self.show_dest_files)

        # Change tabs buttons
        self.back_btn.clicked.connect(lambda : self.tabWidget.setCurrentIndex(1))
        self.edit_paths_btn.clicked.connect(lambda : self.tabWidget.setCurrentIndex(2))

        # Deletion buttons
        self.delete_selected_btn.clicked.connect(self.delete_selected_paths)
        self.delete_all_btn.clicked.connect(self.delete_all_paths)

        # Copy buttons
        self.copy_selected_btn.clicked.connect(self.copy_selected_files)
        self.copy_all_btn.clicked.connect(self.copy_all_files)


    def timer(self):
        # self.timeline = QtCore.QTimeLine()
        # self.timeline.valueChanged.connect(self.doAnim)
        # self.timeline.finished.connect(lambda : self.tabWidget.setCurrentIndex(1))
        # self.timeline.setDuration(1000)
        # self.timeline.start()

        QtCore.QTimer().singleShot(1500,self.doAnim)
        

    def doAnim(self):
        
        
        self.anim1 = QtCore.QPropertyAnimation(self, b"windowOpacity")
        self.anim1.setDuration(400)
        self.anim1.setStartValue(1)
        self.anim1.setEndValue(0)

        self.tabWidget.setCurrentIndex(1)
        self.anim2 = QtCore.QPropertyAnimation(self, b"windowOpacity")
        self.anim2.setDuration(400)
        self.anim2.setStartValue(0)
        self.anim2.setEndValue(1)

        self.squenc_anims = QtCore.QSequentialAnimationGroup() 
        self.squenc_anims.addAnimation(self.anim1)
        self.squenc_anims.addAnimation(self.anim2)

        self.squenc_anims.start(QtCore.QAbstractAnimation.DeleteWhenStopped)



    # Show files in source table files
    @File.varify_path(err_msg ="Source isn't found")
    def show_src_files(self,src_path):
        
        # add path to sources_paths if it isn't existed in.
        if (src_path not in self.file.source_paths):
            self.file.data["Paths"][0]["source_paths"].append(src_path)
            with open("Paths.json","w") as f:
                json.dump(self.file.data,f,indent=2)

        # clear source table file and set row to 0
        self.src_files_table.clearContents()
        self.src_files_table.setRowCount(0)
        self.src_files_table.setColumnCount(2)

        # add files to source table
        src_files = os.listdir(src_path)
        
        # If this file match the regex pattern
        src_files = list(map(lambda item : re.match(self.file.pattern,item.split("/")[-1]),src_files))
        src_files = [item.group() for item in src_files if item != None]
        

        for row, file_ in enumerate(src_files):
            
            full_file_srcpath = os.path.join(self.src_path_comboBox.currentText(),file_)

            # If this path is a file
            if(os.path.isfile(full_file_srcpath)):
                    
                # Take the row position and insert row at this position
                row_position = self.src_files_table.rowCount()
                self.src_files_table.insertRow(row_position)

                # Add file in the table
                self.src_files_table.setItem(row,0,QtWidgets.QTableWidgetItem(file_))

                # Add file modification time
                self.src_files_table.setItem(row,1,QtWidgets.QTableWidgetItem(str(datetime.fromtimestamp(os.stat(full_file_srcpath).st_mtime))))
        
        # reread the paths if any new path add
        self.show_src_dest_paths()

    # Show files in source and destination tables 
    @File.varify_path(err_msg ="Destination isn't found ")
    def show_dest_files(self,dest_path):

        # add path to self.file.destination_paths if it isn't existed in.
        if (dest_path not in self.file.destination_paths):
            self.file.data["Paths"][1]["destination_paths"].append(dest_path)
            with open("Paths.json","w") as f:
                json.dump(self.file.data,f,indent=2)

        # clear destination table file and set row to 0
        self.dest_files_table.clearContents()
        self.dest_files_table.setRowCount(0)
        self.dest_files_table.setColumnCount(2)

        
        # add files to source table
        dest_files = os.listdir(dest_path)

        # If this file match the regex pattern
        dest_files = list(map(lambda item : re.match(self.file.pattern,item.split("/")[-1]),dest_files))
        dest_files = [item.group() for item in dest_files if item != None]
        
        for row, file_ in enumerate(dest_files):
            
            full_file_destpath = os.path.join(self.dest_path_comboBox.currentText(),file_)
            
            # If this path is a file
            if(os.path.isfile(full_file_destpath)):
   
                # Take the row position and insert row at this position
                row_position = self.dest_files_table.rowCount()
                self.dest_files_table.insertRow(row_position)
                
                # Add file in the table
                self.dest_files_table.setItem(row,0,QtWidgets.QTableWidgetItem(str(file_)))

                # Add file modification time
                self.dest_files_table.setItem(row,1,QtWidgets.QTableWidgetItem(str(datetime.fromtimestamp(os.stat(full_file_destpath).st_mtime))))
        
        # reread the paths if any new path add
        self.show_src_dest_paths()

    
    # Show source and destination paths 
    def show_src_dest_paths(self):

        # rereading the source and destination paths
        self.file.read_json_pathfile("Paths.json")

        ####################################################
        # show source paths
        #################
        # add source paths to source comboBox
        # self.src_path_comboBox.clear()
        # self.src_path_comboBox.addItems(self.file.source_paths)
        
        # clear source table file and set row to 0
        self.src_paths_table.clearContents()
        self.src_paths_table.setRowCount(0)
        self.src_paths_table.setColumnCount(1)

        for row, path in enumerate(self.file.source_paths):
  
            # Take the row position and insert row at this position
            row_position = self.src_paths_table.rowCount()
            self.src_paths_table.insertRow(row_position)

            # Add file in the table
            self.src_paths_table.setItem(row,0,QtWidgets.QTableWidgetItem(path))

    
        ####################################################
        # show dest paths
        #################
        # add destination paths to dest comboBox
        # self.dest_path_comboBox.clear()
        # self.dest_path_comboBox.addItems(self.file.destination_paths)

        # clear source table file and set row to 0
        self.dest_paths_table.clearContents()
        self.dest_paths_table.setRowCount(0)
        self.dest_paths_table.setColumnCount(1)

        for row, path in enumerate(self.file.destination_paths):
  
            # Take the row position and insert row at this position
            row_position = self.dest_paths_table.rowCount()
            self.dest_paths_table.insertRow(row_position)

            # Add file in the table
            self.dest_paths_table.setItem(row,0,QtWidgets.QTableWidgetItem(path))

    # Delete selected paths from source and destination
    def delete_selected_paths(self):
        for item in self.src_paths_table.selectedItems():
            self.file.data["Paths"][0]["source_paths"].remove(item.text())
        
        for item in self.dest_paths_table.selectedItems():
            self.file.data["Paths"][1]["destination_paths"].remove(item.text())

        with open("Paths.json",'w') as f:
            json.dump(self.file.data,f,indent=2)

        self.show_src_dest_paths()

    # Delete all paths from source and destination
    def delete_all_paths(self):
        
    
        # Display widget for ensuring the deletion
        cmd = QtWidgets.QMessageBox.question(self,"Delete all Paths","are you sure",
                    QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No ,QtWidgets.QMessageBox.No)

        # if the user accept on deletion -> remove all paths
        if(cmd == QtWidgets.QMessageBox.Yes):           
            
            self.file.data["Paths"][0]["source_paths"].clear()
            self.file.data["Paths"][1]["destination_paths"].clear()
            
            # rewrite the json file
            with open("Paths.json",'w') as f:
                json.dump(self.file.data,f,indent=2)

            # reread the new json file
            self.show_src_dest_paths()

    def copy_selected_files(self):
        
        if(self.src_path_comboBox.currentText() != self.dest_path_comboBox.currentText()):
            for item in self.src_files_table.selectedItems():
                sh.copy(os.path.join(self.src_path_comboBox.currentText(),item.text()),
                            os.path.join(self.dest_path_comboBox.currentText(),item.text()))

            # show the new copied files  
            self.show_dest_files(self.dest_path_comboBox.currentText())

    def copy_all_files(self):
          
        if(self.src_path_comboBox.currentText() != self.dest_path_comboBox.currentText()):
            for i in range(self.src_files_table.rowCount()):
                self.src_files_table.item(i,0).text()

                os.path.join(self.src_files_table.item(i,0).text())

                sh.copy(os.path.join(self.src_path_comboBox.currentText(),self.src_files_table.item(i,0).text()),
                            os.path.join(self.dest_path_comboBox.currentText(),self.src_files_table.item(i,0).text()))

            # show the new copied files  
            self.show_dest_files(self.dest_path_comboBox.currentText())
            

if __name__ == "__main__":
    
    os.environ["QtCore.QT_AUTO_SCREEN_SCALE_FACTOR"] = '2'
    # Enable High DPI display with PyQt5
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)
    main = Main_GUI()
    main.show()
    sys.exit(app.exec_())