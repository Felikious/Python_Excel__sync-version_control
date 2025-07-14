import os
import shutil
from datetime import datetime
from pathlib import Path


class LogManager():

    class LogData():
        
        def __init__(self,start_timestamp,end_timestamp, file_name):
            self.start_timestamp=start_timestamp
            self.end_timestamp=end_timestamp
            self.file_name=file_name


    def __init__(self):
        """Initialize the LogWriter with paths to two files"""
        
        self.code_dir = Path(__file__).parent
        self.logs =""
        self.started=False
        self.

        self.dir_log = self.code_dir/"logs"
        os.makedirs(self.dir_log, exist_ok=True)


    def add(self, message):
        __add_to_log(message)    

    def start(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_filename="logs_of_{t}".format(t=timestamp)        
        backup_path = backup_path / backup_filename
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    def write_and_end(self):
        return None
    
    def read_log(self):
        return None
    