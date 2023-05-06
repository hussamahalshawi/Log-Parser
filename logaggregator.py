from constants import *
class LogAggregator:
    def __init__(self, logs):
        self.logs = logs

    def aggregate(self):
        raise NotImplementedError


class LevelAggregator(LogAggregator):
    def aggregate(self):
        aggregate = []
        levels = {}
        masages = {}
        for log in self.logs:
            level = log['level']
            masage = len(log['masage'])
            levels[level] = levels.get(level, 0) + 1
            masages[level] = masages.get(level, 0) + masage

        for value in levels:
            aggregate.append({'level' : value, 'Num messages': levels[value] , 'Avg length': masages[value]/levels[value] })
        return aggregate


class ModuleAggregator(LogAggregator):
    def aggregate(self):
        aggregate = []
        modules = {}
        masages = {}
        for log in self.logs:
            module = log['module']
            masage = len(log['masage'])
            modules[module] = modules.get(module, 0) + 1
            masages[module] = masages.get(module, 0) + masage

        for value in modules:
            aggregate.append({'module' : value, 'Num messages': modules[value] , 'Avg length': masages[value]/modules[value] })
        return aggregate

class DateAggregator(LogAggregator):
    def aggregate(self):
        aggregate = []
        dates = {}
        masages = {}
        for log in self.logs:
            date = log['date']
            masage = len(log['masage'])
            dates[date] = dates.get(date, 0) + 1
            masages[date] = masages.get(date, 0) + masage

        for value in dates:
            aggregate.append({'date' : value, 'Num messages': dates[value] , 'Avg length': masages[value]/dates[value] })
        return aggregate
