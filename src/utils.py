# src/utils.py
import csv


def csv2coords(csvfile):
    """Extract coordinates from a .csv file"""
    with open(csvfile, 'r') as csvfile:
        next(csvfile)
        csv_reader = csv.reader(csvfile)
        coords = [(float(row[0]), float(row[1])) for row in csv_reader]
    return coords
