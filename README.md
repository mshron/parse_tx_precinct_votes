# Texas precinct vote parsing code

## Background

These scripts were developed by Data 2 the People as part of our work on a Texas senatorial primary. They were targeted for our specific collection format (a very large Google Sheet) but could easily be adapted for use in a more systematic data collection. More than likely these would be a useful starting point or template rather than push-button process for future parsing.

Around half of the counties which submitted their vote totals adhered to a format which could be parsed by these programs. Nevertheless, there are subtle differences between counties, including names of offices and where linebreaks occur in PDFs, which prevented a one-size-fits-all policy. Instead, there are a few control knobs for each kind of parsing, and in practice this was a semi-automated rather than fully-automated process.

## Demo

To see these parsers in action, check out the makefile, or run `make sample_output` which runs each program over a sample input and demonstrates the output format. They're a mix of state machines, PDF parsers, and regular expressions, but they did the trick.
