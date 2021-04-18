REM "Bash file to run test on a linux machine"

ECHO "Running test"
python ../imscraper.py -f ../test/keywords.txt -l 10 -outdir ../test

ECHO "Done"