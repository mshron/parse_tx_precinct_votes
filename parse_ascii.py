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
