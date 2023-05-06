from constants import *
from abc import ABC, abstractmethod
import json
import csv

class FileFormatStrategy(ABC):
    @abstractmethod
    def process_file(self, file, data):
        pass

class CsvFormatStrategy(FileFormatStrategy):
    def process_file(self, file, data):
        keys = data[0].keys()
        try:
            with open(file, 'w', newline ='') as filecsv:
                writer = csv.DictWriter(filecsv, fieldnames = keys)
                writer.writeheader()
                writer.writerows(data)
        except FileNotFoundError:
            print("The file doesn't exist.")        
        except Exception as e:
            print("Error: ", e)        
        

class JsonFormatStrategy(FileFormatStrategy):
    def process_file(self, file, data):
        try:
            with open(file, "w") as filejson:
                json.dump(data, filejson, indent = 4)
        except FileNotFoundError:
            print("The file doesn't exist.")        
        except Exception as e:
            print("Error: ", e)  

class txtFormatStrategy(FileFormatStrategy):
    def process_file(self, file, data):
        keys = data[0].keys()
        try:
            with open(file, "w", newline ='') as filetxt:
                writer = csv.DictWriter(filetxt, fieldnames = keys)
                writer.writeheader()
                writer.writerows(data)
        except FileNotFoundError:
            print("The file doesn't exist.")        
        except Exception as e:
            print("Error: ", e)  

class DataProcessor:
    def __init__(self, strategy: FileFormatStrategy):
        self.set_strategy(strategy)

    def set_strategy(self, strategy: FileFormatStrategy):
        self.strategy = strategy

    def process_file(self, file, data):
        self.strategy.process_file(file, data)


