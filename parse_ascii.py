"""
Parse ascii files of Texas precinct votes

Usage: parse_ascii.py input_file.asc [offset]

We have been pulling data together into a big Google Sheet. This program puts out to standard out. I've been running them manually to see the results, then putting the standard out to a file and importing the file into Google Sheets as a csv.

It turns out that the vote information is encoded in the long numerical string that is in the first column. In all but one case, the vote totals were in positions 12 to 18 (inclusive), left-padded with zeros. In one case they were shifted by 1, so there is an option to put in a shift.

For a faster workflow, use ./test.sh and ./parse.sh to avoid repetition.
"""
import sys
import csv
import re

def clean(row, offset=0):
    row = re.split(r'   +', row)
    votes = str(int(row[0][11+offset:17+offset]))
    race = row[1]
    race = race.replace("DEM ","")
    race = race.replace("Dem ","")
    candidate = row[2]
    precinct = row[3].lower().replace("precinct ","").strip()
    return precinct, race, candidate, votes

def skip(race, candidate):
    race = race.lower()
    candidate = candidate.lower()

    if "president" not in race and \
        "senat" not in race:
            return True

    if "state " in race:
            return True

    if "over" in candidate or \
    "under" in candidate:
        return True

    if "rep " in race:
        return True

    return False


def main():
    filename = sys.argv[1]
    county = filename.split('_')[0]
    offset = int(sys.argv[2])

    results = []
    with open(filename, encoding='latin-1') as f:
        for i, row in enumerate(f):
            try:
                precinct, race, candidate, votes = clean(row, offset)
            except IndexError:
                sys.stdout.write("Skipped malformed row\r")
                continue
            if skip(race, candidate):
                continue
            results.append({'county': county,
                            'precinct': precinct,
                            'race': race,
                            'candidate': candidate,
                            'votes': votes})

    writer = csv.DictWriter(sys.stdout, #(open(out,'w'),
                ["county","","precinct", "race", "candidate", "votes"])
    #writer.writeheader()
    for row in results:
        writer.writerow(row)

if __name__ == "__main__":
    main()
