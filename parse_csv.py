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
