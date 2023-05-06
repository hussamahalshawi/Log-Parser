from outputfile import *


csv_strategy = CsvFormatStrategy()
json_strategy = JsonFormatStrategy()
txt_strategy = txtFormatStrategy()

filecsv = 'Files/outputcsv.csv'
filejson = 'Files/outputjson.json'
filetxt = 'Files/outputtxt.txt'

filter_obj_all = []



regex = r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (INFO|WARN|ERROR|DEBUG) (auth|users|billing) (.+)" # TODO ?P<name>pattern