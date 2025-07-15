    
from pathlib import Path
from Backuper import Backup_Manager
from LogManager import LogManager
from Hasher import Hasher
import os 


class manager:

    def __init__(self):
        """This class manages the backup and logging operations."""
        """It is made so that it can be used in the main.py file, and to log everything that happens in the program."""
        self.hash_manager = Hasher(Path(__file__).parent.parent / "TEST1.xlsx", Path(__file__).parent.parent / "TEST2.xlsx")
        self.backup_Manager = Backup_Manager(Path(__file__).parent.parent / "TEST1.xlsx", Path(__file__).parent.parent / "TEST2.xlsx")
        self.log_manager = LogManager() 


    def start_log(self):
        """Create a log file if it does not exist"""
        self.log_manager.create_log()
        print("Log created successfully.")

    def backup_files(self,AorBorAB):
        """Create backups of fileA, fileB or both based on the input"""
        
        if AorBorAB == "A":
            self.log_manager.log_backup_start("A")
            self.backup_Manager.backup_files("A")
            self.log_manager.log_backup_end()

        if AorBorAB == "B":
            self.log_manager.log_backup_start("B")
            self.backup_Manager.backup_files("B")
            self.log_manager.log_backup_end()

        if AorBorAB == "AB":
            self.log_manager.log_backup_start("AB")
            self.backup_Manager.backup_files("AB")
            self.log_manager.log_backup_end()

        print("Backup completed successfully.")

    def compare_files(self):
        """Compare the files and return the changes"""
        changes_in = self.hash_manager.compare_files()
        self.log_manager.create_log(changes_in)
        return changes_in
