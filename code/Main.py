# This is a project made to help synchronize two excel files
# The way it works at the moment is it hashes the two files and 
# compares the hashes. That way it can notice the changes that happened,
# and change the unchanged file. This is made as a start project
# to make something like a foreign key, on update cascade,
# but across different excel files, and then maybe different type of files.

# author: Felikious 



from all_manager import manager
from pathlib import Path

def demo(mng):
    mng._hash_manager.hash_and_save("AB")


v_demo=True

if v_demo:
    path_file_A = Path(__file__).parent.parent / "File_A_10.xlsx"
    path_file_B = Path(__file__).parent.parent / "File_B_10.xlsx"
else:
    path_file_A = Path(__file__).parent.parent / "File_A_100.xlsx"
    path_file_B = Path(__file__).parent.parent / "File_B_100.xlsx"

if __name__ == "__main__":

    mng = manager(path_file_A, path_file_B)
    demo(mng)

    print("Starting...")
    print("Checking if files were changed...")

    #Check for changed files
    changes_in = mng.start_log_and_compare()

    # If user changed file A, backup file B,   since file B is the one i will be working on
    # If user changed file B, backup file A,   same logic
    # If user changed both files, backup both, same logic

    if changes_in=="A":
        mng.backup_files("B")
    elif changes_in=="B":
        mng.backup_files("A")
    elif changes_in=="AB":
        mng.backup_files("AB")
    else:
        mng.backup_files("AB")

    # Here i need to run the function to change the file 
    # so it matches the other file



    mng.close_log()