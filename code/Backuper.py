import os
import shutil
from datetime import datetime
from pathlib import Path


class Backup_Manager:
    # A class to manage backups of two files
    # It creates a backup of each file in a directory called "backups" in the same directory as this file.

    # Contains a BackupLogManager class to manage logging of backup operations.

    # The methods are:


    #   External methods:
    #  
    # backup_for_changes_in(self, AorBorAB), creates backups of fileA, fileB or both based on the input
    #       and logs the start and end of the backup operation
    # restore_to_most_recent_backup(self, AorBorAB), restores fileA, fileB or both from the most recent backup


    #   Internal methods:

    # __create_backup(file_path, backup_path), creates a timestamped backup of a file
    # __get_most_recent_backup(backup_dir), returns the most recent backup file in
    #       the specified directory or None if no backups exist
    # __backup_files(AorBorAB), creates backups of fileA, fileB or both based on the input



    # LogManager methods:

    # _logging_start(), starts the logging process 
    # _log_file_status(AorBorAB), logs the status of the files before the backup operation
    # _log_backup_start(AorBorAB), logs the start of the backup operation
    # _log_backup_end(), logs the end of the backup operation
    # _logging_end(), ends the logging process



    def __init__(self,fileA_path,fileB_path):
        """Initialize the Backup_Manager with paths to two files"""
        
        # The paths to the files to be backed up
        self.fileA_path = fileA_path
        self.fileB_path = fileB_path

        # Set the directory where this code is located
        self.code_dir = Path(__file__).parent

        # Set/Create the directory for backups
        self.dir_backups = self.code_dir/"backups"
        os.makedirs(self.dir_backups, exist_ok=True)

        # Set/Create directories for backups of each file
        self.dir_backed_fileA = self.dir_backups/"Backups_of_fileA"
        self.dir_backed_fileB = self.dir_backups/"Backups_of_fileB"
        os.makedirs(self.dir_backed_fileA, exist_ok=True)
        os.makedirs(self.dir_backed_fileB, exist_ok=True)

        # Initialize the logger
        self.logger = self.BackupLogManager(self.dir_backups)



    def backup_for_changes_in(self, AorBorAB):
        """Create backups for changes in specified files"""

        self.logger._logging_start()
        self.logger._log_file_status(AorBorAB)

        # If both files have changed, both need to be backed up
        need_to_backup = "AB"
        if AorBorAB == "A" :
            # If only file A has changed, both need to be backed up
            need_to_backup = "B"
        elif AorBorAB == "B":
            # If only file B has changed, both need to be backed up
            need_to_backup = "A"
        
        self.logger._log_backup_start(need_to_backup)
        self.__backup_files(need_to_backup) 
        self.logger._log_backup_end()


    def __create_backup(self, file_path, backup_path):
        """Create timestamped backup of a file, and log the operation"""

        # Create the backup directory
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.basename(file_path)
        backup_filename="{t}_{f}".format(t=timestamp,f=filename)        
        backup_path = backup_path / backup_filename

        # Copy the file to the backup directory
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    
    def __get_most_recent_backup(self, backup_dir):
        """Returns most recent backup file in directory or None if no backups exist"""

        backups = list(backup_dir.glob("*"))
        return max(backups, key=os.path.getmtime, default=None)
    

    def __backup_files(self, AorBorAB):
        """Create backups of fileA, fileB or both based on the input"""
        
        # Start the backup operation
        if AorBorAB=="A" or AorBorAB=="AB" :
            self.__create_backup(self.fileA_path, self.dir_backed_fileA)
        if AorBorAB=="B" or AorBorAB=="AB":
            self.__create_backup(self.fileB_path, self.dir_backed_fileB)
        print("Backup completed successfully.")



    def restore_to_most_recent_backup(self, AorBorAB):
        """Restore fileA, fileB or both from the most recent backup"""
        if AorBorAB == "A" or AorBorAB == "AB":
            recent_backup = self.__get_most_recent_backup(self.dir_backed_fileA)
            shutil.copy2(recent_backup, self.fileA_path)
            print(f"Restored fileA from {recent_backup.name}")
            
        if AorBorAB == "B" or AorBorAB == "AB":
            recent_backup = self.__get_most_recent_backup(self.dir_backed_fileB)
            shutil.copy2(recent_backup, self.fileB_path)
            print(f"Restored fileB from {recent_backup.name}")

        print("Restore completed successfully.")


        # start of the class definition
    # ------------------------------------------------------------------------------------
    #                     BackupLogManager class:
    # ------------------------------------------------------------------------------------
    #                                 A class to manage logging of backup operations

    class BackupLogManager():
        """A class to manage logging of backup operations."""
        """In order to avoid errors as an incomplete backup operation, it logs the start and end of each backup operation."""
        """It also logs the status of the files before and after the backup operation."""

        def __init__(self, dir_backup):
            """Initialize the BackupLogManager with a directory for logs"""
            self.code_dir = Path(__file__).parent   # Directory where this code is located
            self.log_started = False                   # Flag to indicate if logging has started
            self.hanging_backup = False                 # Flag to indicate if there is a hanging backup
            self.dir_log = dir_backup                   
            self.dir_log_file = dir_backup / "backup_log.txt" 
            os.makedirs(self.dir_log_file, exist_ok=True)
            self.__check_old_log_for_hanging_backup()      


        def __check_old_log_for_hanging_backup(self):
            """Check if there is an old log unfinished file/query that indicates a hanging backup operation"""
            if self.dir_log_file.exists():
                with open(self.dir_log_file, 'r') as f:
                    lines = f.readlines()
                    if lines and "Log ended successfully" not in lines[-1] and "Done." not in lines[-2]:
                        self.hanging_backup = True
                        print("Warning: There is a hanging backup operation from a previous run.")
                        self.__correct_hanging_backup()
            else:
                self.hanging_backup = False


        def __correct_hanging_backup(self):
            print("Correcting hanging backup operation...")
            print("Function not implemented yet.")
            # TODO: Implement logic to correct hanging backup operation
            # For now, we will just set the hanging_backup to False
            self.hanging_backup = False

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

    # end of the BackupLogManager class
    # ------------------------------------------------------------------------------------


    
    
   



     
if __name__ == "__main__":
    print("Starting backup...")
    bu=Backup_Manager(Path(__file__).parent.parent / "TEST1.xlsx", Path(__file__).parent.parent / "TEST2.xlsx")
    bu.backup_files("AB")

   