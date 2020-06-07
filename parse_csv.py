"""
Parse csv extracts of Texas precinct vote files.

Usage: cat input.csv | parse_csv.py

Note that this kind of tabular input was rarer, and often came in Excel formats which needed to be exported to CSV for this process. The majority of the well-formatted machine-readable files were pdf and ascii and would have been read by the other programs.

Big picture, this is a simple state machine that tries to figure out where it is in the file based on clues and then parses the candidate names and vote totals as it goes.

We have been pulling data together into a big Google Sheet. This program puts out to standard out. I've been running them manually to see the results, then putting the standard out to a file and importing the file into Google Sheets as a csv.
"""
import sys
import csv
import re

def main():
    results = []
    in_office = False
    for row in csv.reader(sys.stdin):
        if row[1] == '' and \
           re.fullmatch('[0-9]+', row[2]) is not None:
            precinct = row[2]
            in_office = False
        elif row[2] == 'DEM President':
            race = 'President'
            in_office = True
        elif row[2] == 'DEM United States Senator':
            race = 'US Senate'
            in_office = True
        elif row[2] != '' and \
                row[2] != 'Uncommitted' and \
                row[2] != 'Total Votes Cast' and \
                row[5] != '' and \
                in_office:
            candidate = row[2]
            votes = row[5]
            results.append({'precinct': precinct,
                            'race': race,
                            'candidate': candidate,
                            'votes': votes})
        elif row[2] == 'Summary Results Report':
            in_office = False
    writer = csv.DictWriter(sys.stdout, ["precinct", "race", "candidate", "votes"])
    writer.writeheader()
    for row in results:
        writer.writerow(row)

if __name__ == "__main__":
        main()
