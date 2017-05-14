from datetime import datetime as dt
import csv
import json


def read_csv_file(csv_file):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        return json.dumps([dict(zip(headers, row)) for row in reader])


def parse_date(text):
    return dt.strptime(text, "%Y-%m-%d")
