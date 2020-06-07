sample_output/irion_sample.csv:
	python parse_pdf.py sample_input/IRION_COUNTY-2020_MARCH_3RD_DEMOCRATIC_PRIMARY_332020-Precinct\ Results-3-18-2020\ 14-26-56\ PM.pdf sample_output/irion_sample.csv 3 medina

sample_output/bell_sample.csv:
	python parse_ascii.py sample_input/BELL_COUNTY-2020_MARCH_3RD_DEMOCRATIC_PRIMARY_332020-20PBELL.tx 0 > sample_output/bell_sample.csv

sample_output/travis_sample.csv:
	cat sample_input/travis_raw.csv | python parse_csv.py > sample_output/travis_sample.csv

sample_output: sample_output/irion_sample.csv sample_output/bell_sample.csv sample/travis_sample.csv
