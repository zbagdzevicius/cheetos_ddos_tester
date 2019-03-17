import csv
import json

class CsvParser():
    def __init__(self, path_to_file):
        self.json_data = None
        with open( path_to_file) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            self.json_data = self.get_json(csv_reader)
    
    def get_json(self, csv_reader):
        json_data = json.dumps( [ row for row in csv_reader ] )
        json_data = json.loads(json_data, encoding='utf8')
        return json_data