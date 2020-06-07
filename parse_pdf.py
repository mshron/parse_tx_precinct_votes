"""
Parse pdf files of Texas precinct votes

We have been pulling data together into a big Google Sheet. Unlike the other two programs, this one puts out to standard out. It runs much more slowly, since it needs to parse complex pdfs in Java, and it was more convenient to let this run in the background and check result files than it was to run quickly to standard out like the others.

Usage: parse_pdf.py input.pdf output.csv finalpage style

This program parses every page of a pdf (some are over a thousand pages, and can take an hour or more to parse), checking for president or US senate races and moving on otherwise. Because of memory issues, it parses one page at a time, and so needs to be told when to end.

There are, unfortunately, several slight differences by county, each of which has been declared a "style", named after the first county which was in that style. Galveston was the most common style.
"""


import sys

from tabula import read_pdf
import pandas as pd


## Galveston
def parse_president_galveston(df):
    precinct = pd.Series([df.columns[0]]*19)
    names = df[df.columns[0]][2:19]
    votes = df[df.columns[-1]][2:19].str.extract(r'[0-9]+ [0-9.%]+ ([0-9]+)')
    race = pd.Series(['President']*19)
    results = pd.concat([precinct, race, names, votes], axis=1)[2:]
    results.columns = ['precinct', 'race', 'candidates', 'final_votes (number)']
    return(results)

def parse_senator_galveston(df):
    precinct = pd.Series([df.columns[0]]*14)
    names = df[df.columns[0]][2:14]
    votes = df[df.columns[-1]][2:14].str.extract(r'[0-9]+ [0-9.%]+ ([0-9]+)')
    race = pd.Series(['US Senate']*14)
    results = pd.concat([precinct, race, names, votes], axis=1)[2:]
    results.columns = ['precinct', 'race', 'candidates', 'final_votes (number)']
    return(results)

## De Witt
def parse_president_dewitt(df):
    precinct = pd.Series([df.columns[0]]*22)
    names = df[df.columns[0]][3:22]
    names = names.str.replace(r'.*Michael R.*','Michael R. Bloomberg')
    names = names.str.replace(r'.*Rocky.*','Roque "Rocky" De La Fuente')
    votes = df[df.columns[-2]][3:22]
    race = pd.Series(['President']*22)
    results = pd.concat([precinct, race, names, votes], axis=1)[2:].dropna()
    results.columns = ['precinct', 'race', 'candidates', 'final_votes (number)']
    return(results)

def parse_senator_dewitt(df):
    precinct = pd.Series([df.columns[0]]*16)
    names = df[df.columns[0]][3:17].str.extract(r'^([^0-9]+) ')[0]
    names = names.str.replace(r'.*Tzintzun.*','Cristina Tzintzun Ramirez')
    votes = df[df.columns[-2]][3:17]
    race = pd.Series(['US Senate']*16)
    results = pd.concat([precinct, race, names, votes], axis=1)[2:].dropna()
    results.columns = ['precinct', 'race', 'candidates', 'final_votes (number)']
    return(results)

## Medina
def parse_president_medina(df):
    precinct = pd.Series([df.columns[0]]*22)
    names = df[df.columns[0]][3:22]
    names[7] = "Robby Wells"
    names[17] = "Michael Bennet"
    names = names.str.replace(r' [0-9]+.*$','')
    names = names.str.replace(r'.*Michael R.*','Michael R. Bloomberg')
    names = names.str.replace(r'.*Rocky.*','Roque "Rocky" De La Fuente')
    votes = df[df.columns[-2]][3:22]
    race = pd.Series(['President']*22)
    results = pd.concat([precinct, race, names, votes], axis=1)[2:].dropna()
    results.columns = ['precinct', 'race', 'candidates', 'final_votes (number)']
    results.drop
    return(results)

## Potter
def parse_senator_potter(df):
    precinct = pd.Series([df.columns[0]]*14)
    names = df[df.columns[0]][2:14].str.replace(r' [0-9]+.*$','')
    votes = df[df.columns[-1]][2:14].str.extract(r'[0-9]+ [0-9.%]+ ([0-9]+)')
    race = pd.Series(['US Senate']*14)
    results = pd.concat([precinct, race, names, votes], axis=1)[2:]
    results.columns = ['precinct', 'race', 'candidates', 'final_votes (number)']
    return(results)


def main():
    filename = sys.argv[1]
    output = sys.argv[2]
    end_page = int(sys.argv[3])
    style = sys.argv[4]

    if style == "galveston":
        parse_president = parse_president_galveston
        parse_senator = parse_senator_galveston
    elif style == "dewitt":
        parse_president = parse_president_dewitt
        parse_senator = parse_senator_dewitt
    elif style == "medina":
        parse_president = parse_president_medina
        parse_senator = parse_senator_dewitt
    elif style == "potter":
        parse_president = parse_president_galveston
        parse_senator = parse_senator_potter
    else:
        raise

    results = []
    page = 0
    while True:
        page = page + 1
        print(f'page {page} of {end_page}')
        try:
            df = read_pdf(filename, pages = page)[0]
        except IndexError: #nothing to read
            print("Nothing to read on this page")
            continue
        kind = df.iloc[0, 0]
        if 'President' in kind:
            results.append(parse_president(df))
        elif 'U.S. Senator' in kind:
            results.append(parse_senator(df))
        elif 'United States Senator' in kind:
            results.append(parse_senator(df))
        if page == end_page:
            break

    pd.concat(results).to_csv(output, index=False)


if __name__ == "__main__":
    main()
