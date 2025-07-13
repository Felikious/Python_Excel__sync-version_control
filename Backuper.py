import os
import shutil
from datetime import datetime
from pathlib import Path


class Backup_Manager:
    # A class to manage backups of two files
    # It creates a backup of each file in a directory called "backups" in the same directory as this file.
    # The backups are timestamped and saved in subdirectories "Backups_of_fileA" and "Backups_of_fileB".


    def __init__(self,fileA_path,fileB_path):
        """Initialize the Backup_Manager with paths to two files"""
        self.fileA_path = fileA_path
        self.fileB_path = fileB_path

        self.code_dir = Path(__file__).parent

        self.dir_backups = self.code_dir/"backups"
        os.makedirs(self.dir_backups, exist_ok=True)

        self.dir_backed_fileA = self.dir_backups/"Backups_of_fileA"
        self.dir_backed_fileB = self.dir_backups/"Backups_of_fileB"
        os.makedirs(self.dir_backed_fileA, exist_ok=True)
        os.makedirs(self.dir_backed_fileB, exist_ok=True)


    def __create_backup(self, file_path, backup_path):
        """Create timestamped backup of a file"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.basename(file_path)
        backup_filename="{t}_{f}".format(t=timestamp,f=filename)        
        backup_path = backup_path / backup_filename
        shutil.copy2(file_path, backup_path)
        return backup_path
    

    def backup_files(self, AorBorAB):
        """Create backups of fileA, fileB or both based on the input"""
        if AorBorAB=="A" or AorBorAB=="AB" :
            self._create_backup(self.fileA_path, self.dir_backed_fileA)
        if AorBorAB=="B" or AorBorAB=="AB":
            self._create_backup(self.fileB_path, self.dir_backed_fileB)
        print("Backup completed successfully.")
    
    def restore_file(self, AorBorAB):
        return 0 



    
        
if __name__ == "__main__":
    print("Starting backup...")
    bu=Backup_Manager(Path(__file__).parent.parent / "TEST1.xlsx", Path(__file__).parent.parent / "TEST2.xlsx")
    bu.backup_files("AB")