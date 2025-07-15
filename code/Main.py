from all_manager import manager





if __name__ == "__main__":

    mng = manager()

    print("Starting...")
    print("Checking if files were changed...")

    #Check for changed files

    changes_in = hash_manager.compare_files()
    log_manager.create_log(changes_in)

    if changes_in=="-":
        print("nothing changed")
        
    if changes_in=="A":
        print("File A")



    if changes_in=="B":
        print("File B")
        backup_files("A")

    if changes_in=="AB":
        print("File AB")
        backup_files("AB")

    log_manager.close_log()




