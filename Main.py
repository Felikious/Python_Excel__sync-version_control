from Hasher import Hasher
from Backuper import Backup_Manager
from pathlib import Path

if __name__ == "__main__":

    hash_manager   = Hasher(Path(__file__).parent.parent / "TEST1.xlsx", Path(__file__).parent.parent / "TEST2.xlsx")
    backup_Manager = Backup_Manager(Path(__file__).parent.parent / "TEST1.xlsx", Path(__file__).parent.parent / "TEST2.xlsx")



    print("Starting...")
    print("Checking if files were changed...")
    #Check for changed files
    changes_in = hash_manager.compare_files()
    if changes_in=="-":
        print("nothing changed")
        #LOG
    if changes_in=="A":
        print("File A")
        backup_Manager.backup_files("B")
    if changes_in=="B":
        print("File B")
        backup_Manager.backup_files("A")
    if changes_in=="AB":
        print("File B")
        backup_Manager.backup_files("AB")

