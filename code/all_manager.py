    
from pathlib import Path
from Backuper import Backup_Manager
from LogManager import LogManager
from Hasher import Hasher
import os 


class manager:

    def __init__(self,file_A_path, file_B_path):
        """This class manages the complex operations."""
        """It is made so that it can be used in the main.py file, and to log everything that happens in the program."""
        self._hash_manager = Hasher(file_A_path, file_B_path)
        self._backup_manager = Backup_Manager(file_A_path, file_B_path)
        self._log_manager = LogManager() 

    def start_log_and_compare(self):
        """Compare the files and return which changed"""
        changes_in = self._hash_manager.compare_files()
        self._log_manager.create_log(changes_in)
        return changes_in
    


    def backup_files(self,AorBorAB):
        """Create backups of fileA, fileB or both based on the input, and log the operation."""
        
        if AorBorAB == "A":
            self._log_manager.log_backup_start("A")
            self._backup_manager.backup_files("A")
            self._log_manager.log_backup_end()

        if AorBorAB == "B":
            self._log_manager.log_backup_start("B")
            self._backup_manager.backup_files("B")
            self._log_manager.log_backup_end()

        if AorBorAB == "AB":
            self._log_manager.log_backup_start("AB")
            self._backup_manager.backup_files("AB")
            self._log_manager.log_backup_end()

        print("Backup completed successfully.")


    def close_log(self):
        """Close the log file"""
        self._log_manager.close_log()
        print("Log closed successfully.")

    
