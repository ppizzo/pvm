import mylib
import db
import sys
import subprocess

def plot_daily_details(date):
    """Daily details plot"""

    file = open("data.plot", mode="w")

    result = db.read_daily_details(date)
    for row in result:
        for field in row[:-1]:
            print(field, end="", file=file)
            print("\t", end="", file=file)
        print(row[-1:][0], file=file)
