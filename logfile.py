from constants import *
from abc import ABC, abstractmethod

class LogFile(ABC):
    def __init__(self, filename):
        self.filename = filename
        
    def read(self):
        try:
            with open(self.filename, 'r') as filelog:
                log_entries = filelog.readlines()
        except FileNotFoundError:
            log_entries = []
            print("The file doesn't exist.")        
        except Exception as e:
            print("Error: ", e)        
        return log_entries

