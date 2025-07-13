


class LogWriter():

    def __init__(self):
        """Initialize the LogWriter with paths to two files"""
        
        self.code_dir = Path(__file__).parent

        self.dir_backups = self.code_dir/"logs"
        os.makedirs(self.dir_backups, exist_ok=True)

        self.dir_backed_fileA = self.dir_backups/"Backups_of_fileA"
        self.dir_backed_fileB = self.dir_backups/"Backups_of_fileB"
        os.makedirs(self.dir_backed_fileA, exist_ok=True)
        os.makedirs(self.dir_backed_fileB, exist_ok=True)

    def add_to_log():
        return None
    
    def start_log():
        return None
    
    def end_log():
        return None
    
    def 