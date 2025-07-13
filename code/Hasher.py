import hashlib as hl
import zipfile as zf
import os
from pathlib import Path



class Hasher:
    # a class with methods to hash two excel files and compare them
    # it uses the sha256 algorithm to hash the files
    # it saves the hashes in a directory called "active_hashes" in the same directory as this file

    #The methods are:

    #  External methods:
    # hash_and_save(AorBorAB): hashes the files and saves the hashes in the active_hashes directory
    # compare_files(): compares the current hashes with the saved hashes and returns
    #                 a string showing which files were changed

    #  Internal methods:
    # __hash_file(file_path): hashes a single file and returns the hash
    # __hash_files(): hashes both files and returns the hashes
    # __read_saved_hashes(): reads the saved hashes from the files




    def __init__(self, fileA_path, fileB_path):
        self.fileA_path = fileA_path
        self.fileB_path = fileB_path

        code_dir = Path(__file__).parent
        dir_active_hashes = code_dir/"active_hashes"

        self.hash_fileA_path = dir_active_hashes / "hashA.bin"
        self.hash_fileB_path = dir_active_hashes / "hashB.bin"

        os.makedirs(dir_active_hashes, exist_ok=True)


    def __hash_file(self, file_path):
        # hashes a single file and returns the hash
        sha256 = hl.sha256()
        
        with zf.ZipFile(file_path, 'r') as zip_ref:
            for file in sorted(zip_ref.namelist()):
                if file.startswith('xl/worksheets/sheet'):
                    with open(file_path, 'rb') as f:
                        while True:
                            data = f.read(65536) #It reads 64Kb per loop
                            if not data:
                                break
                            sha256.update(data)

        my_hash = sha256.digest()
        print("\nSHA256 of file\""+ str(file_path)+ "\" was:\n {0}".format((my_hash.hex())))
        #print("SHA256 of file\""+ str(file_path)+ "\" was: {0}".format(str(bytes.fromhex(my_hash))))
        return my_hash
    
    def __hash_files(self):
        # hashes both files and returns the hashes
        return self.__hash_file(self.fileA_path),self.__hash_file(self.fileB_path)
    
    def __read_saved_hashes(self):
        # reads the saved hashes from the files and returns them
        with open(self.hash_fileA_path, "rb") as bin_file:
            a_bin= bin_file.read()
        with open(self.hash_fileB_path, "rb") as bin_file:
            b_bin= bin_file.read()
        return a_bin,b_bin
    
    def hash_and_save(self, AorBorAB):
        # hashes the files and saves the hashes in the active_hashes directory
        if AorBorAB=="A" or AorBorAB=="AB" :
            with open(self.hash_fileA_path, "wb") as bin_file:
                bin_file.write(self.__hash_file(self.fileA_path))
        if AorBorAB=="B" or AorBorAB=="AB":
            with open(self.hash_fileB_path, "wb") as bin_file:
                bin_file.write(self.__hash_file(self.fileB_path))
    

    
    def compare_files(self):
        # returns a string showing which files were changed
        # "-" if none, "A" if fileA changed, "b" for fileB
        # and "AB" if both of them changed 
        current_hash_a,current_hash_b = self.__hash_files()
        saved_hash_a  , saved_hash_b  = self.__read_saved_hashes()
        
        a_changed=(current_hash_a != saved_hash_a)
        b_changed=(current_hash_b != saved_hash_b)

        if   ((not a_changed) and (not b_changed)):
            print("all same")
            return "-"
        elif ((a_changed)and (not b_changed)):
            print("file A changed")
            return "A"
        elif ((not a_changed) and  (b_changed)):
            print("file B changed")
            return "B"
        else:
            print("You are kinda screwed")
            return "AB"




# Example usage
if __name__ == "__main__":
    print("Starting synchronization...")
    vc=Hasher(Path(__file__).parent.parent / "TEST1.xlsx", Path(__file__).parent.parent / "TEST2.xlsx")
    vc.hash_and_save("AB")
    vc.__hash_file(vc.fileA_path)
    vc.__hash_file(vc.fileB_path)
    vc.compare_files()

    
    
