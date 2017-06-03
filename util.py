from datetime import datetime as dt
from os.path import join, isdir
import csv
import json


def read_csv_file(csv_file):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        return [dict(zip(headers, row)) for row in reader]


def parse_date(text):
    return dt.strptime(text, "%Y-%m-%d")


def is_git_dir(git_dir):
    git_dot_dir = join(git_dir, ".git")
    return isdir(git_dot_dir)
