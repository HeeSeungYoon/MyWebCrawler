from PyQt5.QtCore import *

class Worker(QThread):
    saving = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        
    def run(self):
        self.saving.emit(1)

    def stop(self):
        self.quit()    
        self.wait(5000)
        
        