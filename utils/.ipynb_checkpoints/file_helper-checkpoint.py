import os
import pandas as pd
from datetime import datetime as dt
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

class FileHandler:
    """
    save the file as csv 
    read the csv file
    """    
    @staticmethod
    def csv_reader(file_name, dir_name, folder_name=""):
        """
        save file path 
        data/dir_name/yyyy-mm/folder_name/file_name.csv
        dir_name = raw or proceed or interim
        folder_name = plan_summary or day_late etc ...
        """
        
        _path = os.getenv("DEFAULT")
        print("path_name : ",_path)
        print(dotenv_path)
        _dir_name = dir_name
        print("dir_name : ",_dir_name)
        _folder_name = folder_name if len(folder_name) != 0 else ""
        _child_path = "_".join([str(dt.now().year), str(dt.now().month)])
        _file_path = os.path.join(_path, 'data', _dir_name, _child_path, _folder_name)
        _file_name = "_".join([file_name, str(dt.now().year), str(dt.now().month), str(dt.now().day)])
        _read_file_path = os.path.join(_file_path, _file_name)
        _read_csv = ".".join([_read_file_path,"csv"])
        print("read_file : ",_read_csv)

        return pd.read_csv(_read_csv, dtype={'customer_id': str},low_memory=False)

    
    @staticmethod
    def saved_as_csv(dataframe, file_name, dir_name, folder_name=""):
        """
        result dir structure
        data/dir_name/yyyy-mm/folder_name/file_name.csv
        result dataframe
        order by customer_id
        """  
        _df = dataframe.copy()
        _path = os.getenv('DEFAULT')
        _file_name = file_name
        _dir_name = dir_name
        _folder_name = folder_name if len(folder_name) != 0 else ""
        _parent_path = os.path.join(_path, 'data', _dir_name)
        _child_path = "_".join([str(dt.now().year), str(dt.now().month)])
        _full_path = os.path.join(_parent_path, _child_path, _folder_name)
        if not os.path.isdir(_full_path):
            os.makedirs(_full_path, exist_ok=False)
        _out_raw = "_".join([_file_name,str(dt.now().year),str(dt.now().month),str(dt.now().day)])
        _output_file_path = os.path.join(_full_path,_out_raw)
        _output_file = ".".join([_output_file_path,"csv"])
        _df_n = _df.sort_values(by='customer_id')
        _df_n.to_csv(_output_file, index=False)
        
    @staticmethod
    def snapshot_save(dataframe, file_name):
        _df = dataframe.copy()
        _path = os.getenv('DEFAULT')
        _file_name = file_name
        _dir_name = 'snapshot'
        _parent_path = os.path.join(_path, 'data', _dir_name)
        _output_file_path = os.path.join(_parent_path,_file_name)
        _output_file = ".".join([_output_file_path,"csv"])
        _df_n = _df.sort_values(by='customer_id')
        _df_n.to_csv(_output_file, index=False)
        
    @staticmethod
    def snapshot_read(file_name):
        _path = os.getenv('DEFAULT')
        _file_name = file_name
        _dir_name = 'snapshot'
        _file_path = os.path.join(_path, 'data', _dir_name, _file_name)
        _read_csv = ".".join([_file_path,"csv"])
        return pd.read_csv(_read_csv, dtype={'customer_id': str},low_memory=False)
    
    @staticmethod
    def external_file_reader(file_name):
        _file_name = file_name
        _path = os.getenv('DEFAULT')
        _file_name = file_name
        _dir_name = 'external'
        _file_path = os.path.join(_path, 'data', _dir_name, _file_name)
        _read_csv = ".".join([_file_path,"csv"])
        return pd.read_csv(_read_csv)
        
        
        
        
        
        