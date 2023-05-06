from constants import *
from abc import ABC, abstractmethod

class LogFilter:
    @abstractmethod
    def process_filter(self, file):
        pass
class LevelFilter(LogFilter):
    def __init__(self, level):
        self.level = level
    def process_filter(self, data):
        return [log for log in data if log['level'] == self.level]

class ModuleFilter(LogFilter):
    def __init__(self, module):
        self.module = module
    def process_filter(self, data):
        return [log for log in data if log['module'] == self.module]
    
class DateFilter(LogFilter):
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
    def process_filter(self, data):
        return [log for log in data if self.start_date <= log['date'] <= self.end_date]

class DataFilter:
    def __init__(self, strategy: LogFilter):
        self.set_strategy(strategy)


    def set_strategy(self, strategy: LogFilter):
        self.strategy = strategy

    def process_filter(self, data):
        return self.strategy.process_filter(data)
