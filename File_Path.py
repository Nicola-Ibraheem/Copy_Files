import os
import sys
import json

from PyQt5.QtWidgets import QMessageBox

class File():
        
    def __init__(self):
        self.data, self.source_paths, self.destination_paths = None, None, None
        self.pattern = r"(\w|\s|-_\(\))+\.(docx|pdf|txt)\Z"
        # self.pattern = r"(\.[docx|pdf|txt]+)$"

        self.read_json_pathfile("Paths.json")

    def create_json_pathfile(self,file_name):

        st = """
        {
            "Paths": [
                {
                "source_paths": [
                ]
                },
                {
                "destination_paths": [
                ]
                }
            ]
        }
        """
        # If the json file_name doesn't exist then we will add it.
        if(os.path.exists(file_name)==False):

            with open(file_name,"w") as f:   
                data = json.loads(st)
                json.dump(data,f,indent=2)
            

        
        self.read_json_pathfile(file_name)
    
    def read_json_pathfile(self,file_name):
        # try to open json file_name
        try:
            with open(file_name,"r") as f:
                data = json.load(f)
        except FileNotFoundError:
            QMessageBox.warning(None,"NOT FOUND","json file isn't found by programe\n"
                "A new file will be created")
            
            # cmd = QMessageBox.question(self,"NOT FOUND","json file isn't found by programe\n"
            #     "A new file will be created",QMessageBox.Yes|QMessageBox.No, 
            #     QMessageBox.No)
            
            # if(cmd == QMessageBox.Yes):

            self.create_json_pathfile(file_name)
        else:
            self.data, self.source_paths, self.destination_paths =  data, data["Paths"][0]["source_paths"] , data["Paths"][1]["destination_paths"]
   
    @staticmethod
    def varify_path(err_msg):
        def outer(func):
            def inner(*args,**kwargs):
                
                target_path = args[1]
                
                # check if the path are exist
                try:
                    if(os.path.exists(target_path)==False):
                        raise FileNotFoundError
                    
                except FileNotFoundError:
                    QMessageBox.warning(None,"NOT FOUND",err_msg)
                    # logger.exception("{} {}".format(err_msg,err.__traceback__.tb_lineno))

                else:
                    func(*args,**kwargs)       
            return inner
        return outer

