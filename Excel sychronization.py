# This is a project made to help synchronize two excel files
# The way it works at the moment is it checks the two files and a 
# hidden version control file. It notices the changes that happened,
# and changes the unchanged file. This is made as a start project 
# to make something like a foreign key, on update cascade,
# but across different excel files, and then maybe different type of files.

# author: Felikious 

import pandas as pd
import numpy as np
import hashlib as hl
import zipfile as zf
import sys
import os
import shutil
from datetime import datetime
from collections import defaultdict

class Excel_Version_Control:

    def __init__(self, project_path, fileA_name, fileB_name):
        self.fileA_path = project_path +"/"+fileA_name
        self.fileB_path = project_path +"/"+fileB_name
        
    #CVould use here a thingy to choose between fast hash pr slow hash (remember metada)
    hasher = Hash_Controller()
    a_changed = hasher._is_file_changed(path_file_a)
    b_changed = hasher._is_file_changed(path_file_b)

    


