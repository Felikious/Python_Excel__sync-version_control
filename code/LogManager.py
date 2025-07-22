import os
import shutil
from datetime import datetime
from pathlib import Path



"""TODO ADD READING OF LOG FILES AND BACKUPS AND RESTORING FROM THEM"""

class BackupLogManager():
    """A class to manage logging of messages to a file.
    It creates a log file in a directory called "logs" in the same directory as this file.
    The log file is timestamped and saved in the "logs" directory."""  
        
    def __init__(self):
        """Does not take any arguments."""

        
        self.code_dir = Path(__file__).parent
        self.log_started=False
        self.hanging_backup=False
        self.dir_log = self.code_dir/"logs"
        self.hanging_add = False
        os.makedirs(self.dir_log, exist_ok=True)


    def create_log(self, AorBorABorNone=None):
        """Create a log file if it does not exist"""
        if self.log_started:
            print("Log already created.")
            return
        self.__create_log()
        self.__write_file_status(AorBorABorNone)
        self.log_started = True
        self.hanging_backup = False
        self.hanging_add = False
        print("Log created successfully.")

    def log_backup_start(self, AorBorAB):
        """Start a backup operation and log it"""
        if not self.log_started:
            print("Log not created yet. Please create a log first.")
            return
        if self.hanging_backup:
            print("Backup already started.")
            return
        self.__log_backup_start(AorBorAB)
        self.hanging_backup = True
        print("Logged backup start for: {}".format(AorBorAB))

    def log_backup_end(self):
        """End a backup operation and log it"""
        if not self.hanging_backup or not self.log_started:
            print("No backup or log operation started.")
            return
        self.__log_backup_end()
        self.hanging_backup = False
        print("Logged backup end")

    def add_start(self, file, row, column, oldvalue, newvalue):
        """Start an add operation and log it"""
        if not self.log_started:
            print("Log not created yet. Please create a log first.")
            return
        if self.hanging_backup:
            print("Hanging backup operation already exists. Please close it before starting a new one.")
            return
        if self.hanging_add:
            print("Hanging add operation already exists. Please close it before starting a new one.")
            return
        
        self.__add_start(file, row, column, oldvalue, newvalue)
        self.hanging_add = True
        print("Add operation started successfully.")

    def add_close(self):
        """End an add operation and log it"""
        if not self.hanging_add or not self.log_started or not self.hanging_backup:
            print("No add operation started.")
            return
        self.__add_close()
        self.hanging_add = False
        print("Add operation ended successfully.")

    def close_log(self):
        """Close the log file"""
        if not self.log_started:
            print("Log not created yet. Please create a log first.")
            return
        if self.hanging_backup or self.hanging_add:
            print("Please close all ongoing operations before closing the log.")
            return
        self.__close_log()
        self.log_started = False
        print("Log closed successfully.")

    def log_hash_update(self, file, old_hash, new_hash):
        """Log a hash update for a file""" 
        print("Feature not implemented yet.")
        # This method can be implemented to log hash updates for files.
        # It will mostly be used by humans to check  how the program functions.
 
    def __create_log(self):
        """Create a timestamped log file"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = "log_{t}.txt".format(t=timestamp)
        self.log_file = self.dir_log / log_filename
        with open(self.log_file, 'w') as f:
            f.write("Log started at {t}\n".format(t=timestamp))

    def __write_file_status(self, AorBorABorNone):
        """Write the status of the files to the log file"""
        with open(self.log_file, 'a') as f:
            if AorBorABorNone == "A":
                f.write("Changes detected at file A.\n")
            elif AorBorABorNone == "B":
                f.write("Changes detected at file B.\n")
            elif AorBorABorNone == "AB":
                f.write("Changes detected at both files A and B.\n")
            else:
                f.write("No changes were detected in any file.\n")


    def __log_backup_start(self, AorBorAB):
        """Write a header to the log file"""
        with open(self.log_file, 'a') as f:
            if AorBorAB=="A" or AorBorAB=="B":
                f.write("Backup operation for: {} ...".format(AorBorAB))
            elif AorBorAB=="AB":
                f.write("Backup operation for both files A and B ...")

    def __log_backup_end(self):
        """Write a footer to the log file"""
        with open(self.log_file, 'a') as f:
            f.write(" Done.\n")

    def __add_start(self, file, row, column, oldvalue, newvalue):
        with open(self.log_file, 'a') as f:
            f.write("\nAdding edit to file: {}\n".format(file))
            f.write("Row: {}, Column: {}\n".format(row, column))
            f.write("Old Value: {}\n".format(oldvalue))
            f.write("New Value: {}\n".format(newvalue))
                
    def __add_close(self):
        with open(self.log_file, 'a') as f:
            f.write("Done\n")

    def __close_log(self):
        """Write a footer to the log file"""
        with open(self.log_file, 'a') as f:
            f.write("Log ended at {t}\n".format(t=datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))


class BackupLogManager():
    """A class to manage logging of messages to a file.
    It creates a log file in a directory called "logs" in the same directory as this file.
    The log file is timestamped and saved in the "logs" directory."""  
        
    def __init__(self,dir_backup):
        """Does not take any arguments."""
        self.code_dir = Path(__file__).parent
        self.log_started = False
        self.hanging_backup = False
        self.dir_log = dir_backup
        self.dir_log_file = dir_backup / "backup_log.txt"
        os.makedirs(self.dir_log_file, exist_ok=True)

    def _logging_start(self):
        """Create a timestamped log query"""
        if self.log_started or self.hanging_backup:
            print("Log already started or backup operation is in progress.")
            return -1
        with open(self.dir_log_file, 'a') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            f.write("Log started at {t}\n".format(t=timestamp))
        self.log_started = True

    def _log_file_status(self, AorBorABorNone):
        """Write the status of the files to the log file"""
        with open(self.dir_log_file, 'a') as f:
            if AorBorABorNone == "A":
                f.write("Changes detected at file A.\n")
            elif AorBorABorNone == "B":
                f.write("Changes detected at file B.\n")
            elif AorBorABorNone == "AB":
                f.write("Changes detected at both files A and B.\n")
            else:
                f.write("No changes were detected in any file.\n")


    def _log_backup_start(self, AorBorAB):
        """Write a header to the log file"""
        with open(self.dir_log_file, 'a') as f:
            if AorBorAB == "A" or AorBorAB == "B":
                f.write("Backup operation for: {} ...".format(AorBorAB))
            else:
                f.write("Backup operation for both files A and B ...")
            

    def _log_backup_end(self):
        """Write a footer to the log file"""
        with open(self.dir_log_file, 'a') as f:
            f.write(" Done.\n")

    def _logging_end(self):
        """Write a footer to the log file"""
        with open(self.dir_log_file, 'a') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            f.write("Log ended successfully at {t}\n".format(t=timestamp))
        self.log_started = False
   