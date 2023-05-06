from constants import *
from logfile import LogFile
from logaggregator import LevelAggregator, ModuleAggregator, DateAggregator
from logfilter import DataFilter, LevelFilter, ModuleFilter, DateFilter
from outputfile import *
import re
import argparse


def operations():
    parser = argparse.ArgumentParser(description='Command-line tool for managing log parser data.')
    parser.add_argument('-f','--file', help='the path to the JSON file containing the product data', required=True)
    parser.add_argument('-o', '--output', help='Output', metavar=('typesave'))
    parser.add_argument('-l', '--level', help='level', metavar=('name'))
    parser.add_argument('-m', '--module', help='module', metavar=('name'))
    parser.add_argument('-d', '--date', help='date', nargs=2, metavar=('start_date', 'end_date'))
    parser.add_argument('-a', '--aggregation', help='Aggregation', metavar=('name'))
    

    args = parser.parse_args()

    if args.file:
        if args.file is not None :
            loadfile = LogFile(filename = args.file)
            data = loadfile.read()
            listdata = regular_data(data)
        else:
            print("The Value Error")
    if args.level or args.module or args.date :
        if args.level:
            if args.level is not None :
                filter_obj = DataFilter(LevelFilter(args.level))
                value = filter_obj.process_filter(listdata)
                append_filter_obj_all(value)
                # print(filter_obj.filters)
            else:
                print("The Value Name Level Error")

        if args.module:
            if args.module is not None :
                filter_obj = DataFilter(ModuleFilter(args.module))
                value = filter_obj.process_filter(listdata)
                append_filter_obj_all(value)
                # print(filter_obj.filters)
            else:
                print("The Value Name Module Error")
        if args.date:
            if args.date is not None :
                filter_obj = DataFilter(DateFilter(args.date[0],args.date[1]))
                value = filter_obj.process_filter(listdata)
                append_filter_obj_all(value)
                # print(filter_obj.filters)
            else:
                print("The Value Date Error")
    else:
        append_filter_obj_all(listdata)
    
    if args.aggregation:
        if args.aggregation == 'level':
            aggregator = LevelAggregator(filter_obj_all)
            aggregate_ = aggregator.aggregate()
            # print(aggregator.aggregate())
        elif args.aggregation == 'module':
            aggregator = ModuleAggregator(filter_obj_all)
            aggregate_ = aggregator.aggregate()
            # print(aggregator.aggregate())
        elif args.aggregation == 'date':
            aggregator = DateAggregator(filter_obj_all)
            aggregate_ = aggregator.aggregate()
            # print(aggregator.aggregate())
        else:
            print("Invalid aggregation type specified.")


    if args.output:
        save_data(typesave = args.output, data = aggregate_)

        
def append_filter_obj_all(value):
    for filter_value in value:
        if filter_value not in filter_obj_all:
            filter_obj_all.append(filter_value)
        else:
            print("The Value in list")
        

def regular_data(data):
    '''
    spilt data to dictionaries

    Args:
        data (list): A list of string data.

    
    '''
    list_data = []
    for string in data:
        regex_ = re.match(regex, string)
        list_data.append({'date':regex_[1],'level':regex_[3],'module':regex_[4],'masage':regex_[5]})
    # print(list_data)
    return list_data




def save_data(typesave, data):
    '''
    Write file

    Args:
        typesave (str): a type data save
        data (list of dice): A dice data.

    
    '''

    if typesave == "json":
        processor = DataProcessor(json_strategy)
        processor.process_file(filejson, data)
    elif typesave == "csv":
        processor = DataProcessor(csv_strategy)
        processor.process_file(filecsv, data)
    elif typesave == "txt":
        processor = DataProcessor(txt_strategy)
        processor.process_file(filetxt, data)
    elif typesave == "*":
        print(data)
    else:
        print("Not type save")
    



if __name__ == "__main__":

    operations()

























'''Task: Log Parser
You are tasked with developing a log parser that extracts and analyzes data from server log files. The log files contain lines of text in the following format:
timestamp] [level] [module] [message]
where:
timestamp: a string representing the date and time in the format "YYYY-MM-DD HH:MM:SS"
level: a string representing the log level, which can be one of the following: "DEBUG", "INFO", "WARN", or "ERROR"
module: a string representing the module name that generated the log message
message: a string representing the log message itself
Your task is to implement a log parser that reads a log file, extracts relevant information, and performs analysis on the log data. The parser should support the following features:
Filtering: The parser should be able to filter the log messages based on one or more criteria, such as log level, module name, or date range.
Aggregation: The parser should be able to aggregate the log data based on one or more criteria, such as log level or module name, and calculate statistics such as the number of log messages, average message length, and so on.
Output: The parser should be able to output the results of the analysis in various formats, such as CSV, JSON, or plain text.
To implement this task, you should use the following guidelines:
Define a LogEntry class that represents a single log entry, with fields for timestamp, level, module, and message.
Implement a regular expression pattern that matches a single log entry and use it to extract the relevant information from each line in the log file.
Define an abstract LogFilter class that encapsulates the filtering logic, and implement concrete subclasses for each type of filter (level filter, module filter, date range filter, etc.). Use the strategy design pattern to allow the parser to dynamically select the appropriate filter based on user input.
Define an abstract LogAggregator class that encapsulates the aggregation logic, and implement concrete subclasses for each type of aggregator (level aggregator, module aggregator, etc.). Use the strategy design pattern to allow the parser to dynamically select the appropriate aggregator based on user input.
Implement a LogFile class that represents a log file, with methods for reading the file and returning a list of LogEntry objects.
Implement a LogParser class that takes a LogFile object as input, applies the appropriate filters and aggregators based on user input, and returns the results of the analysis in the desired output format.
Implement a command-line interface that allows the user to specify the log file, filters, aggregators, and output format, and displays the results of the analysis on the console or writes them to a file.
Example usage:
python log_parser.py -f server.log -l ERROR -m auth -a module -o csv
This command should parse the file server.log, filter the log entries to only include those with log level ERROR and module name auth, aggregate the log entries by module name, and output the results in CSV format.
Module,Num messages,Avg length
auth,37,45.6
users,24,78.2
billing,10,64.5
This output shows the number of log messages and the average length of messages for each module that generated log entries with a log level of ERROR within the specified date range. The output is in CSV format, as specified by the -o csv command-line argument. Note that the output format and the specific fields displayed can be customized based on user input.
Input Example
2023-05-01 12:30:15 DEBUG auth User authenticated successfully
2023-05-01 13:45:22 INFO users User profile updated
2023-05-01 14:02:03 WARN billing Payment failed: Insufficient funds
2023-05-02 08:15:11 ERROR auth Login failed: Invalid credentials
2023-05-02 09:30:30 ERROR users Unable to load user profile: database connection error
2023-05-02 11:15:02 ERROR billing Payment failed: Credit card expired
2023-05-03 14:05:19 ERROR auth Login failed: Account locked
2023-05-03 15:20:41 WARN users User account suspended: Exceeded login attempts
2023-05-03 16:45:10 INFO billing Payment received: Order #1234'''